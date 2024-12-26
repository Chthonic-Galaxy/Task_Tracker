# This module contains the TaskManager class, which handles task management operations.

import pathlib  # Import the pathlib module for working with file paths.
import json  # Import the json module for encoding and decoding JSON data.
from datetime import datetime  # Import the datetime class for working with dates and times.

from task_tracker.core.exceptions import EmptyStorage, StorageNotExists  # Import custom exception classes.

class TaskManager:
    """
    Manages tasks by providing functionalities to add, update, delete, mark, and list tasks.
    It persists task data in a JSON file.
    """

    def __init__(self, command: str) -> None:
        """
        Initializes the TaskManager with the given command and sets up the storage paths.

        Args:
            command (str): The command to be executed (e.g., 'add', 'update', 'list').
        """
        self.command = command  # Store the command.
        self.storage_path = pathlib.Path("./tasks.json")  # Define the path for the main task storage file.

        # Create the storage file if it doesn't exist.
        if not self.storage_path.exists():
            with open(self.storage_path, "w"):
                pass

        self.map_path = pathlib.Path("./map.json") # Define the path for the task ID to status map file.
        self.map = self.__load_map() # Load the task ID to status map from the file.

    def __call__(self, *args, **kwds):
        """
        Makes the TaskManager instance callable, executing the corresponding command.

        Args:
            *args: Positional arguments passed to the command handler.
            **kwds: Keyword arguments passed to the command handler.

        Returns:
            The result of the executed command handler.
        """
        commands = {
            "add": self.add_task,
            "update": self.update_task,
            "delete": self.delete_task,
            "marking": self.task_marking,
            "list": self.task_list
        }
        return commands[self.command](*args, **kwds)

    def __load_map(self) -> dict:
        """
        Loads the task ID to status mapping from the map file.

        Returns:
            dict: A dictionary mapping task IDs to their current status.
        """
        try:
            data = self.__validate(self.map_path, existence=True, contents=True) # Validate and load the map file.
            return data
        except Exception:
            return {} # Return an empty dictionary if loading fails.

    def add_task(self, description: str) -> None:
        """
        Adds a new task to the storage.

        Args:
            description (str): The description of the task.
        """
        task_id = 0  # Initialize the task ID.
        tasks = self.__validate(existence=True, contents=True)  # Load existing tasks from storage.
        # Determine the next available task ID.
        if tasks and len(self.map):
            task_id = max(int(task_id) for task_id in self.map) + 1

        task = {
            "description": description,
            "status": "todo",
            "createdAt": datetime.now().isoformat(),
            "updatedAt": datetime.now().isoformat()
        }

        tasks = self.__mapper(task_id, tasks=tasks, task=task, dest="todo") # Add the new task to the tasks dictionary and update the map.

        self._write_data_into_storage(tasks, self.storage_path)  # Write the updated tasks to the storage file.

        print(f"Task added successfully (ID: {task_id})")

    def update_task(self, task_id: str, description: str) -> None:
        """
        Updates the description of an existing task.

        Args:
            task_id (str): The ID of the task to update.
            description (str): The new description for the task.
        """
        tasks = self.__validate(existence=True, contents=True, task_id=task_id)  # Load tasks and validate the existence of the task ID.
        task = tasks[self.map[task_id]][task_id] # Get the task details.
        task = {
            "description": description,
            "status": task["status"],
            "createdAt": task["createdAt"],
            "updatedAt": datetime.now().isoformat()
        }

        tasks = self.__mapper(task_id, tasks=tasks, task=task, dest=self.map[task_id]) # Update the task in the tasks dictionary.

        self._write_data_into_storage(tasks, self.storage_path)  # Write the updated tasks to the storage file.

    def delete_task(self, task_id: str) -> None:
        """
        Deletes a task from the storage.

        Args:
            task_id (str): The ID of the task to delete.
        """
        tasks = self.__validate(existence=True, contents=True, task_id=task_id)  # Load tasks and validate the existence of the task ID.
        tasks = self.__mapper(task_id, tasks=tasks, delete=True)  # Remove the task from the tasks dictionary and update the map.

        self._write_data_into_storage(tasks, self.storage_path)  # Write the updated tasks to the storage file.

    def task_marking(self, task_id: str, status: str) -> None:
        """
        Marks a task with the given status.

        Args:
            task_id (str): The ID of the task to mark.
            status (str): The new status of the task ('todo', 'in-progress', 'done').
        """
        tasks = self.__validate(existence=True, contents=True, task_id=task_id)  # Load tasks and validate the existence of the task ID.
        task = tasks[self.map[task_id]][task_id] # Get the task details.
        task = {
            "description": task["description"],
            "status": status,
            "createdAt": task["createdAt"],
            "updatedAt": datetime.now().isoformat()
        }

        tasks = self.__mapper(task_id, tasks=tasks, task=task, dest=status) # Update the task status in the tasks dictionary and update the map.

        self._write_data_into_storage(tasks, self.storage_path)  # Write the updated tasks to the storage file.

    def task_list(self, status: str | None = None) -> None:
        """
        Lists tasks, optionally filtered by status.

        Args:
            status (str | None): The status to filter tasks by ('done', 'todo', 'in-progress'). If None, list all tasks.
        """
        tasks = self.__validate(existence=True, contents=True)  # Load tasks from storage.

        if not status:
            # If no status is provided, list all tasks.
            for task_id, src in self.map.items():
                print(tasks[src][task_id]["description"])
            return

        # List tasks with the specified status.
        for task in tasks[status].values():
            print(task["description"])

    def __validate(self, file: pathlib.Path | None = None, *, existence: bool = True, contents: bool = False, strict: bool = False, task_id: str | None = None) -> dict | None:
        """
        Validates the storage file and its contents.

        Args:
            file (pathlib.Path | None): The path to the file to validate. Defaults to self.storage_path.
            existence (bool): If True, checks if the file exists. Defaults to True.
            contents (bool): If True, checks if the file has valid JSON content. Defaults to False.
            strict (bool): If True, raises exceptions on validation errors. Defaults to False.
            task_id (str | None): If provided, checks if the task ID exists in the map. Defaults to None.

        Returns:
            dict | None: The loaded data if contents is True, otherwise None.

        Raises:
            StorageNotExists: If the storage file does not exist and existence is True.
            EmptyStorage: If the storage file is empty and contents is True.
            IndexError: If a task_id is provided but not found in the map.
        """
        data = {}
        file = file or self.storage_path # Use provided file path or default storage path.

        if existence:
            if not file.exists():
                raise StorageNotExists
        if contents:
            with open(file, "r", encoding="utf-8") as storage:
                try:
                    data = json.load(storage)
                except json.decoder.JSONDecodeError as e:
                    if strict:
                        raise
                    print(e)
                if not data:
                    try:
                        raise EmptyStorage
                    except EmptyStorage as e:
                        if strict:
                            raise
                        else:
                            print(f"[IGNORE] {e}")
                            tasks = {}
        if task_id is not None:
            if task_id not in self.map:
                raise IndexError(f"There is not task ID {task_id} in storage.")

        return data

    def __mapper(
        self,
        task_id: int,
        *,
        tasks: dict,
        task: dict | None = None,
        dest: str = "todo",
        delete: bool = False
    ) -> dict:
        """
        Manages the task's location within the different status lists and updates the map.

        Args:
            task_id (int): The ID of the task.
            tasks (dict): The dictionary containing tasks grouped by status.
            task (dict | None): The task data. Required when adding or updating a task. Defaults to None.
            dest (str): The destination status for the task ('todo', 'in-progress', 'done'). Defaults to "todo".
            delete (bool): If True, deletes the task. Defaults to False.

        Returns:
            dict: The updated tasks dictionary.
        """
        tasks = tasks or {"todo": {}, "in-progress": {}, "done": {}} # Initialize tasks dictionary if empty.
        src = self.map.get(str(task_id)) # Get the current status of the task from the map.
        if src is None:
            # If the task is new, add it to the destination status list and update the map.
            self.map[str(task_id)] = dest
            tasks[dest][str(task_id)] = task
        else:
            if not delete:
                # If not deleting, move or update the task.
                if src != dest:
                    # Move the task to the new status list.
                    migrant = tasks[src].pop(str(task_id))
                    tasks[dest][str(task_id)] = migrant

                    self.map[str(task_id)] = dest # Update the task's status in the map.
                else:
                    # Update the task in its current status list.
                    tasks[src][str(task_id)] = task
            else:
                # If deleting, remove the task from its current status list and the map.
                del tasks[src][str(task_id)]
                del self.map[str(task_id)]
        return tasks

    def _write_data_into_storage(self, data: dict, storage: str | pathlib.Path) -> None:
        """
        Writes the given data to the specified storage file in JSON format.

        Args:
            data (dict): The data to write to the storage.
            storage (str | pathlib.Path): The path to the storage file.
        """
        with open(storage, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
