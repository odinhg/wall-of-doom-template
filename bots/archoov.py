import argparse
from pathlib import Path
from datetime import datetime
import re

def to_console(message: str, name: str = "archoov"):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {name} >> {message}")

if __name__ == "__main__":
    to_console("Starting archiving process...")

    parser = argparse.ArgumentParser(description="Archive completed tasks from WALL.md")
    parser.add_argument("wall_path", type=str, help="Path to WALL.md file")
    parser.add_argument("archive_dir", type=str, help="Path to archive directory")
    args = parser.parse_args()
    wall_path = Path(args.wall_path).resolve()
    archive_dir = Path(args.archive_dir).resolve()

    if not archive_dir.exists():
        archive_dir.mkdir(parents=True, exist_ok=True)
        to_console(f"Created archive directory at {archive_dir}")

    if not wall_path.exists():
        to_console(f"WALL.md not found at {wall_path}")
        raise FileNotFoundError(f"WALL.md not found at {wall_path}")

    archived_time = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    archive_path = archive_dir / f"WALL_{archived_time}.md"


    with wall_path.open("r", encoding="utf-8") as f:
        lines = f.readlines()

    section_header_pattern = re.compile(r"^##\s+.*")
    completed_task_pattern = re.compile(r"^\s*[-*]\s+\[x\].*")
    incomplete_task_pattern = re.compile(r"^\s*[-*]\s+\[ \].*")
    new_wall = []
    archived_wall = []
    complete_count = 0
    incomplete_count = 0
    section = None

    for line in lines:
        if completed_task_pattern.match(line):
            archived_wall.append(line)
            complete_count += 1
        elif incomplete_task_pattern.match(line):
            new_wall.append(line)
            incomplete_count += 1
        elif section_header_pattern.match(line):
            new_wall.append(line)
            archived_wall.append(line)
            section = line.strip("## ").strip()
            to_console(f"Processing section \"{section}\"")
        else:
            archived_wall.append(line)
            new_wall.append(line)
    
    to_console(f"Archiving {complete_count} completed tasks.")
    to_console(f"Remaining {incomplete_count} incomplete tasks in WALL.md.")

    with archive_path.open("w", encoding="utf-8") as f:
        f.writelines(archived_wall)
        to_console(f"Archived WALL.md written to {archive_path}")
    with wall_path.open("w", encoding="utf-8") as f:
        f.writelines(new_wall)
        to_console(f"Updated WALL.md written to {wall_path}")

    to_console("Archiving process completed. See you next time!")


