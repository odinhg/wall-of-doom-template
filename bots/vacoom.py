import argparse
from pathlib import Path
from datetime import datetime
import re

"""
Vacoom does two things and operates only on `WALL.md`:

1. Move done tasks to the bottom of each task list.
2. Sort every task list by priority.

For example, given the following `WALL.md` content:

# My Section

Here is some text. Whatever.

- [ ] Hello!
- [x] (2) This is done.
- [ ] (1) This is important.
- [x] (3) This is also done.
- [ ] (4) This is less important.
- [ ] (2) Almost very important.

After running `vacoom.py WALL.md`, the content will be transformed to:

# My Section

Here is some text. Whatever.

- [ ] (1) This is important.
- [ ] (2) Almost very important.
- [ ] Hello! <-- since no priority is given (3)
- [ ] (4) This is less important.
- [x] (2) This is done.
- [x] (3) This is also done.

"""


def to_console(message: str, name: str = "vacoom"):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {name} >> {message}")

if __name__ == "__main__":
    to_console("Let me tidy up your list a bit...")

    parser = argparse.ArgumentParser(description="Archive completed tasks from WALL.md")
    parser.add_argument("wall_path", type=str, help="Path to WALL.md file")
    args = parser.parse_args()
    wall_path = Path(args.wall_path).resolve()

    if not wall_path.exists():
        to_console(f"WALL.md not found at {wall_path}")
        raise FileNotFoundError(f"WALL.md not found at {wall_path}")

    with wall_path.open("r", encoding="utf-8") as f:
        lines = f.readlines()

    section_header_pattern = re.compile(r"^##\s+.*")
    task_pattern = re.compile(r"^\s*[-*]\s+\[( |x)\].*")

    new_wall = []
    section = None
    task_list = []

    def process_task_list(task_list):
        incomplete_tasks = []
        complete_tasks = []

        priority_pattern = re.compile(r"\((\d+)\)")

        for task in task_list:
            match = priority_pattern.search(task)
            priority = int(match.group(1)) if match else 3
            if task.strip().startswith(("- [x]", "* [x]")):
                complete_tasks.append((priority, task))
            else:
                incomplete_tasks.append((priority, task))
        incomplete_tasks.sort(key=lambda x: x[0])
        complete_tasks.sort(key=lambda x: x[0])
        sorted_tasks = [task for _, task in incomplete_tasks + complete_tasks]
        return sorted_tasks

    for line in lines:
        if task_pattern.match(line):
            task_list.append(line)
        else:
            if task_list:
                sorted_tasks = process_task_list(task_list)
                new_wall.extend(sorted_tasks)
                task_list = []
            new_wall.append(line)
            if section_header_pattern.match(line):
                section = line.strip("## ").strip()
                to_console(f"Processing section \"{section}\"")

    if task_list:
        sorted_tasks = process_task_list(task_list)
        new_wall.extend(sorted_tasks)

    with wall_path.open("w", encoding="utf-8") as f:
        f.writelines(new_wall)

    to_console("Tidying complete!")
