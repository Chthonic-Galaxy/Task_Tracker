import argparse  # Import the argparse module for parsing command-line arguments.

from task_tracker.core.task_manager import TaskManager  # Import the TaskManager class from the core module.

# Initialize parser
parser = argparse.ArgumentParser()  # Create an ArgumentParser object to handle command-line arguments.
subparser = parser.add_subparsers(dest="command")  # Create sub-parsers for different commands, the chosen command will be stored in the 'command' attribute.

# Set up commands
# 'add' command: for adding a new task.
add_parser = subparser.add_parser("add")  # Create a sub-parser for the 'add' command.
add_parser.add_argument("description")  # Add an argument 'description' to the 'add' command, which will hold the task description.

# 'update' command: for updating an existing task.
update_parser = subparser.add_parser("update")  # Create a sub-parser for the 'update' command.
update_parser.add_argument("task_id")  # Add an argument 'task_id' to the 'update' command to specify the task to update.
update_parser.add_argument("description")  # Add an argument 'description' to the 'update' command for the new description.

# 'delete' command: for deleting a task.
delete_parser = subparser.add_parser("delete")  # Create a sub-parser for the 'delete' command.
delete_parser.add_argument("task_id")  # Add an argument 'task_id' to the 'delete' command to specify the task to delete.

# 'mark-in-progress' command: for marking a task as in progress.
mark_in_progress = subparser.add_parser("mark-in-progress")  # Create a sub-parser for the 'mark-in-progress' command.
mark_in_progress.add_argument("task_id")  # Add an argument 'task_id' to specify the task to mark.

# 'mark-done' command: for marking a task as done.
mark_done = subparser.add_parser("mark-done")  # Create a sub-parser for the 'mark-done' command.
mark_done.add_argument("task_id")  # Add an argument 'task_id' to specify the task to mark.

# 'list' command: for listing tasks based on their status.
list_parser = subparser.add_parser("list")  # Create a sub-parser for the 'list' command.
list_parser.add_argument("status", nargs="?", choices=["done", "todo", "in-progress"])  # Add an optional 'status' argument with allowed choices.

if __name__ == "__main__":
    args = parser.parse_args().__dict__  # Parse the command-line arguments and convert the result to a dictionary.

    # Modify arguments for 'mark-in-progress' and 'mark-done' commands for easier processing.
    if args["command"] in ("mark-in-progress", "mark-done"):
        # If the command is 'mark-in-progress', set the 'status' to 'in-progress'.
        # Otherwise, if the command is 'mark-done', set the 'status' to 'done'.
        args["status"] = "in-progress" if args["command"] == "mark-in-progress" else "done"
        args["command"] = "marking"  # Change the command to 'marking' for unified handling.

    # Initialize the TaskManager with the command to be executed.
    tm = TaskManager(args.pop("command"))  # Remove the 'command' from the arguments dictionary and pass it to the TaskManager.
    tm(**args)  # Call the TaskManager instance as a function, passing the remaining arguments.
    tm._write_data_into_storage(tm.map, tm.map_path) # Write the updated task map to the storage file after command execution.
