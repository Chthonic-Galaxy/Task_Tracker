import argparse

from core.task_manager import TaskManager

# Initialize parser
parser = argparse.ArgumentParser()
subparser = parser.add_subparsers(dest="command")

# Set up commands
add_parser = subparser.add_parser("add")
add_parser.add_argument("description")

update_parser = subparser.add_parser("update")
update_parser.add_argument("task_id")
update_parser.add_argument("description")

delete_parser = subparser.add_parser("delete")
delete_parser.add_argument("task_id")


mark_in_progress = subparser.add_parser("mark-in-progress")
mark_in_progress.add_argument("task_id")

mark_done = subparser.add_parser("mark-done")
mark_done.add_argument("task_id")


list_parser = subparser.add_parser("list")
list_parser.add_argument("status", nargs="?", choices=["done", "todo", "in-progress"])

if __name__ == "__main__":
    args = parser.parse_args().__dict__
    
    if args["command"] in ("mark-in-progress", "mark-done"):
        args["status"] = "in-progress" if args["command"] == "mark-in-progress" else "done"
        args["command"] = "marking"
    
    tm = TaskManager(args.pop("command"))
    tm(**args)
