import pathlib
import json
from datetime import datetime

from task_tracker.core.exceptions import EmptyStorage, StorageNotExists


class TaskManager:
    
    def __init__(self, command):
        self.command = command
        self.storage_path = pathlib.Path("./tasks.json")
        
        if not self.storage_path.exists():
            with open(self.storage_path, "w"):
                pass
        
        self.map_path = pathlib.Path("./map.json")
        self.map = self.__load_map()
    
    def __call__(self, *args, **kwds):
        commands = {
            "add": self.add_task,
            "update": self.update_task,
            "delete": self.delete_task,
            "marking": self.task_marking,
            "list": self.task_list
        }
        return commands[self.command](*args, **kwds)
        
    
    
    def __load_map(self):
        print(f"[LOADING] map({self.map_path})")
        try:
            data = self.__validate(self.map_path, existence=True, contents=True)
            print("[LOADED] map")
            return data
        except Exception:
            print("[ERROR] loading map")
            return {}
    
    
    def add_task(self, description: str):
        
        task_id = 0
        tasks = self.__validate(existence=True, contents=True)
        if tasks:
            task_id = max(int(task_id) for task_id in self.map) + 1
        
        task = {
            "description": description,
            "status": "todo",
            "createdAt": datetime.now().isoformat(),
            "updatedAt": datetime.now().isoformat()
        }
        
        tasks = self.__mapper(task_id, tasks=tasks, task=task, dest="todo")
        
        self._write_data_into_storage(tasks, self.storage_path)
        
        print(f"Task added successfully (ID: {task_id})")
        
    def update_task(self, task_id: str, description: str):
        
        tasks = self.__validate(existence=True, contents=True, task_id=task_id)
        task = tasks[self.map[task_id]][task_id]
        task = {
            "description": description,
            "status": task["status"],
            "createdAt": task["createdAt"],
            "updatedAt": datetime.now().isoformat()
        }
        
        tasks = self.__mapper(task_id, tasks=tasks, task=task, dest=self.map[task_id])
        
        self._write_data_into_storage(tasks, self.storage_path)
    
    def delete_task(self, task_id: str):
        
        tasks = self.__validate(existence=True, contents=True, task_id=task_id)
        tasks = self.__mapper(task_id, tasks=tasks, delete=True)
        
        self._write_data_into_storage(tasks, self.storage_path)
        
    def task_marking(self, task_id: str, status: str):
        
        tasks = self.__validate(existence=True, contents=True, task_id=task_id)
        task = tasks[self.map[task_id]][task_id]
        task = {
            "description": task["description"],
            "status": status,
            "createdAt": task["createdAt"],
            "updatedAt": datetime.now().isoformat()
        }
        
        tasks = self.__mapper(task_id, tasks=tasks, task=task, dest=status)
        
        self._write_data_into_storage(tasks, self.storage_path)
    
    def task_list(self, status=None):
        
        tasks = self.__validate(existence=True, contents=True)
        
        if not status:
            for task_id, src in self.map.items():
                print(tasks[src][task_id]["description"])
            return
        
        for task in tasks[status].values():
            print(task["description"])

    def __validate(self, file: pathlib.Path | None = None, *, existence: bool = True, contents: bool = False, strict: bool = False, task_id: None | int = None) -> dict | None:
        
        data = {}
        file = file or self.storage_path
        
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
    ):
        tasks = tasks or {"todo": {}, "in-progress": {}, "done": {}}
        src = self.map.get(task_id)
        if src is None:
            self.map[task_id] = dest
            tasks[dest][task_id] = task
        else:
            if not delete:
                if src != dest:
                    migrant = tasks[src].pop(task_id)
                    tasks[dest][task_id] = migrant
                    
                    self.map[task_id] = dest
                else:
                    tasks[src][task_id] = task
            else:
                del tasks[src][task_id]
                del self.map[task_id]
        return tasks
            
    
    def _write_data_into_storage(self, data: dict, storage: str | pathlib.Path):
        with open(storage, "w", encoding="utf-8") as storage:
            json.dump(data, storage, indent=4, ensure_ascii=False, sort_keys=True)
