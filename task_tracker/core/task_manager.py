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
            "marking": self.task_marking
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
        self._write_data_into_storage(tasks, storage)
        
        print(f"Task added successfully (ID: {task_id})")
        
    def update_task(self, task_id: str, description: str):
        
        if self.storage_path.exists():
            with open(self.storage_path, "r", encoding="utf-8") as storage:
                try:
                    tasks = json.load(storage)
                    if not tasks:
                        raise EmptyStorage
                except json.decoder.JSONDecodeError:
                    pass
                except EmptyStorage as e:
                    print(e)
        else:
            try:
                raise StorageNotExists
            except StorageNotExists as e:
                print(e)
                return
        

        try:
            if task_id not in tasks:
                raise IndexError(f"There is not task ID {task_id} in storage.")
        except IndexError as e:
            print(e)
            return
        
        
        task = tasks[task_id]
        
        tasks[task_id] = {
            "description": description,
            "status": task["status"],
            "createdAt": task["createdAt"],
            "updatedAt": datetime.now().isoformat()
        }
        
        self._write_data_into_storage(tasks, storage)
    
    def delete_task(self, task_id: str):
        
        if self.storage_path.exists():
            with open(self.storage_path, "r", encoding="utf-8") as storage:
                try:
                    tasks = json.load(storage)
                    if not tasks:
                        raise EmptyStorage
                except json.decoder.JSONDecodeError:
                    pass
                except EmptyStorage as e:
                    print(e)
        else:
            try:
                raise StorageNotExists
            except StorageNotExists as e:
                print(e)
                return
        

        try:
            if task_id not in tasks:
                raise IndexError(f"There is not task ID {task_id} in storage.")
        except IndexError as e:
            print(e)
            return
        
        del tasks[task_id]
        
        self._write_data_into_storage(tasks, storage)
        
    def task_marking(self, task_id: str, status: str):
        
        if self.storage_path.exists():
            with open(self.storage_path, "r", encoding="utf-8") as storage:
                try:
                    tasks = json.load(storage)
                    if not tasks:
                        raise EmptyStorage
                except json.decoder.JSONDecodeError:
                    pass
                except EmptyStorage as e:
                    print(e)
        else:
            try:
                raise StorageNotExists
            except StorageNotExists as e:
                print(e)
                return
        

        try:
            if task_id not in tasks:
                raise IndexError(f"There is not task ID {task_id} in storage.")
        except IndexError as e:
            print(e)
            return
        
        
        task = tasks[task_id]
        
        tasks[task_id] = {
            "description": task["description"],
            "status": status,
            "createdAt": task["createdAt"],
            "updatedAt": datetime.now().isoformat()
        }
        
        self._write_data_into_storage(tasks, storage)
            
    def _write_data_into_storage(self, tasks: dict, storage: str | pathlib.Path):
        with open(self.storage_path, "w", encoding="utf-8") as storage:
            json.dump(tasks, storage, indent=4, ensure_ascii=False)
