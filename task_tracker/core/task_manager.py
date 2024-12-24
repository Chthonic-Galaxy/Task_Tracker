import pathlib
import json
from datetime import datetime


class TaskManager:
    
    def __init__(self, command):
        self.command = command
        self.storage_path = pathlib.Path("./tasks.json")
        
        if not self.storage_path.exists():
            with open(self.storage_path, "w"):
                pass
    
    def __call__(self, *args, **kwds):
        commands = {
            "add": self.add_task
        }
        return commands[self.command](*args, **kwds)
        
        
    def add_task(self, description: str):
        
        task_id = 0
        tasks = {}
        if self.storage_path.exists():
            with open(self.storage_path, "r", encoding="utf-8") as storage:
                try:
                    tasks = json.load(storage)
                    task_id = max(int(task) for task in tasks) + 1
                except json.decoder.JSONDecodeError:
                    pass
        
        task = {
            "description": description,
            "status": "todo",
            "createdAt": datetime.now().isoformat(),
            "updatedAt": datetime.now().isoformat()
        }
        
        tasks[task_id] = task
        with open(self.storage_path, "w", encoding="utf-8") as storage:
            json.dump(tasks, storage, indent=4, ensure_ascii=False)
