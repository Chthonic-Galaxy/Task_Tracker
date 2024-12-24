import argparse

# Initialize parser
parser = argparse.ArgumentParser()
subparser = parser.add_subparsers(dest="command")

# Set up commands
add_parser = subparser.add_parser("add")
add_parser.add_argument("task_description")

update_parser = subparser.add_parser("update")
update_parser.add_argument("task_id", type=int)
update_parser.add_argument("task_description")

delete_parser = subparser.add_parser("delete")
delete_parser.add_argument("task_id", type=int)

list_parser = subparser.add_parser("list")
list_parser.add_argument("status", nargs="?", choices=["done", "todo", "in-progress"])


args = parser.parse_args()

