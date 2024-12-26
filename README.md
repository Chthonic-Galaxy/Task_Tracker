# 🚀 Task Tracker - Your Simple Command-Line Task Manager

Keep your life organized with the Task Tracker, a lightweight and easy-to-use command-line tool for managing your tasks. Whether it's grocery lists, project deadlines, or personal reminders, Task Tracker helps you stay on top of things without the clutter of a full-fledged application.

## ✨ Features

* **Add Tasks:** Easily add new tasks with a descriptive text.
* **Update Tasks:** Modify the description of existing tasks.
* **Delete Tasks:** Remove tasks that are no longer relevant.
* **Mark Tasks:** Transition tasks through different statuses:
    * **To Do:** Tasks that need to be started.
    * **In Progress:** Tasks that are currently being worked on.
    * **Done:** Tasks that have been completed.
* **List Tasks:** View your tasks, optionally filtered by their status (to do, in progress, or done).
* **Simple Data Storage:**  Task data is stored in JSON files (`tasks.json` and `map.json`) for persistence.

## 🛠️ Installation

Before you begin, make sure you have Python 3.6 or higher installed on your system.

1. **Clone the repository:**

   ```bash
   git clone https://github.com/Chthonic-Galaxy/Task_Tracker.git
   cd task-tracker
   ```

2. **Install dependencies using Poetry (recommended):**

   This project uses [Poetry](https://python-poetry.org/) for dependency management. If you don't have Poetry installed, you can install it by following the instructions on their website.

   ```bash
   poetry install
   ```

   This will create a virtual environment and install all the necessary packages.

3. **Alternatively, install dependencies using pip:**

   If you prefer using `pip`, you can install the dependencies from the `pyproject.toml` file:

   ```bash
   pip install -r pyproject.toml
   ```

   **Note:** While the `pyproject.toml` lists the build dependencies for Poetry, this approach might require manual management of runtime dependencies if they were added later. Using Poetry is the recommended way to ensure consistency.

## 🕹️ Usage

The Task Tracker is a command-line tool. You can run it using the `task_tracker/main.py` script.

**Basic Command Structure:**

```bash
python task_tracker/main.py <command> [arguments]
```

**Available Commands:**

* **`add`**: Add a new task.
   ```bash
   python task_tracker/main.py add "Buy groceries for the week"
   ```
   Output:
   ```
   Task added successfully (ID: 0)
   ```

* **`update`**: Update the description of an existing task. Requires the `task_id` and the new `description`.
   ```bash
   python task_tracker/main.py update 0 "Buy organic groceries for the week"
   ```

* **`delete`**: Delete a task. Requires the `task_id`.
   ```bash
   python task_tracker/main.py delete 0
   ```

* **`mark-in-progress`**: Mark a task as in progress. Requires the `task_id`.
   ```bash
   python task_tracker/main.py mark-in-progress 1
   ```

* **`mark-done`**: Mark a task as done. Requires the `task_id`.
   ```bash
   python task_tracker/main.py mark-done 1
   ```

* **`list`**: List all tasks or tasks with a specific status.
    * List all tasks:
      ```bash
      python task_tracker/main.py list
      ```
      Output (example):
      ```
      Buy organic groceries for the week
      Finish writing the project report
      Walk the dog
      ```
    * List tasks with a specific status (`todo`, `in-progress`, `done`):
      ```bash
      python task_tracker/main.py list todo
      ```
      Output (example):
      ```
      Buy organic groceries for the week
      ```

## 📂 Project Structure

```
.
├── README.md          <- This file
├── map.json           <- Stores the mapping of task IDs to their status
├── poetry.lock        <- Dependency lock file for Poetry
├── poetry.toml        <- Project configuration and dependencies for Poetry
├── pyproject.toml     <- Project configuration (used by Poetry and other tools)
├── task.md            <- (Potentially a scratchpad or notes - could be removed or repurposed)
├── task_tracker
│   ├── __init__.py    <- Makes 'task_tracker' a Python package
│   ├── core
│   │   ├── __init__.py
│   │   ├── exceptions.py <- Custom exception classes
│   │   └── task_manager.py <- Core logic for managing tasks
│   └── main.py        <- Entry point for the command-line interface
└── tasks.json         <- Stores the actual task data
```

## 🤝 Contributing

Contributions are welcome! If you have suggestions for improvements or find any bugs, feel free to open an issue or submit a pull request.

Here's how you can contribute:

1. **Fork the repository.**
2. **Create a new branch** for your feature or bug fix.
3. **Make your changes** and commit them with clear, concise messages.
4. **Push your branch** to your forked repository.
5. **Submit a pull request** to the main repository.

---

**Enjoy managing your tasks with Task Tracker!**
