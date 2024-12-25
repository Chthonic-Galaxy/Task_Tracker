import pathlib
import json
from datetime import datetime

from core.exceptions import EmptyStorage, StorageNotExists


class TaskManager:
    
    def __init__(self, command):
        self.command = command
        self.storage_path = pathlib.Path("./tasks.json")
        
        if not self.storage_path.exists():
            with open(self.storage_path, "w"):
                pass
    
    def __call__(self, *args, **kwds):
        commands = {
            "add": self.add_task,
            "update": self.update_task,
            "delete": self.delete_task,
            "marking": self.task_marking,
            "list": self.task_list
        }
        return commands[self.command](*args, **kwds)
        
        
    def add_task(self, description: str):
        
        task_id = 0
        tasks = self.__validate(existence=True, contents=True)
        if tasks:
            task_id = max(int(task) for task in tasks) + 1
        
        task = {
            "description": description,
            "status": "todo",
            "createdAt": datetime.now().isoformat(),
            "updatedAt": datetime.now().isoformat()
        }
        
        tasks[task_id] = task
        self._write_data_into_storage(tasks, self.storage_path)
        
        print(f"Task added successfully (ID: {task_id})")
        
    def update_task(self, task_id: str, description: str):
        
        tasks = self.__validate(existence=True, contents=True, task_id=task_id)
        
        task = tasks[task_id]
        
        tasks[task_id] = {
            "description": description,
            "status": task["status"],
            "createdAt": task["createdAt"],
            "updatedAt": datetime.now().isoformat()
        }
        
        self._write_data_into_storage(tasks, self.storage_path)
    
    def delete_task(self, task_id: str):
        
        tasks = self.__validate(existence=True, contents=True, task_id=task_id)
        
        del tasks[task_id]
        
        self._write_data_into_storage(tasks, self.storage_path)
        
    def task_marking(self, task_id: str, status: str):
        
        tasks = self.__validate(existence=True, contents=True, task_id=task_id)
        
        task = tasks[task_id]
        
        tasks[task_id] = {
            "description": task["description"],
            "status": status,
            "createdAt": task["createdAt"],
            "updatedAt": datetime.now().isoformat()
        }
        
        self._write_data_into_storage(tasks, self.storage_path)
    
    def task_list(self, status=None):
        
        tasks = self.__validate(existence=True, contents=True)
        
        if not status:
            for task in tasks.values():
                print(task["description"])
            return
        
        for task in filter(lambda task_def: task_def["status"] == status, tasks.values()):
            print(task["description"])
    
    def __validate(self, existence: bool = True, contents: bool = False, strict: bool = False, task_id: None | int = None) -> dict | None:
        
        tasks = {}
        
        if existence:
            if not self.storage_path.exists():
                raise StorageNotExists
        if contents:
            with open(self.storage_path, "r", encoding="utf-8") as storage:
                try:
                    tasks = json.load(storage)
                except json.decoder.JSONDecodeError as e:
                    if strict:
                        raise
                    print(e)
                if not tasks:
                    try:
                        raise EmptyStorage
                    except EmptyStorage as e:
                        if strict:
                            raise
                        else:
                            print(f"[IGNORE] {e}")                    
                            tasks = {}
        if task_id is not None:
            if task_id not in tasks:
                raise IndexError(f"There is not task ID {task_id} in storage.")
        
        return tasks
        
    
    def __mapper(self, task: dict, tasks: dict, storage: str | pathlib.Path):
        ...
    
    def _write_data_into_storage(self, tasks: dict, storage: str | pathlib.Path):
        with open(self.storage_path, "w", encoding="utf-8") as storage:
            json.dump(tasks, storage, indent=4, ensure_ascii=False)
