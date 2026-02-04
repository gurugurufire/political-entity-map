import os
import datetime
import argparse
import re
from pathlib import Path

def create_task(title, priority, root_dir, detailed=True):
    safe_title = re.sub(r'[\\/*?:"<>|]', "", title).replace(" ", "_")
    date_str = datetime.date.today().strftime("%Y-%m-%d")
    filename = f"{date_str}-{safe_title}.md"
    
    taskboard_path = Path(root_dir) / "TaskBoard.md"
    tasks_dir = Path(root_dir) / ".agent" / "plans" / "tasks"
    
    rel_task_path = f".agent/plans/tasks/{filename}"
    
    if detailed:
        tasks_dir.mkdir(parents=True, exist_ok=True)
        task_path = tasks_dir / filename
        
        content = f"""# 📝 Task: {title}
- **Status**: 🏗️ In Progress
- **Created**: {date_str}
- **Priority**: {priority}

## 🎯 Goal
(タスクの目的を記述)

## 📋 Subtasks
- [ ] 
- [ ] 

## 📓 Notes
- 

---
Created by task-manager skill
"""
        with open(task_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"✅ Created detailed task file: {task_path}")
        link = f"[{title}]({rel_task_path})"
    else:
        link = title

    update_taskboard(link, priority, taskboard_path)

def update_taskboard(link, priority, taskboard_path):
    if not taskboard_path.exists():
        content = "# AI Research Lab - Task Board\n\n## 🚀 Active Tasks\n"
        with open(taskboard_path, "w", encoding="utf-8") as f:
            f.write(content)

    with open(taskboard_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Find the best insertion point (e.g., under a specific header)
    # For simplicity, we'll look for "### 🚀 直近のメインタスク" or just add to the top of the first list under a header
    new_entry = f"- [ ] **{link}** (Priority: {priority})\n"
    
    inserted = False
    for i, line in enumerate(lines):
        if "直近のメインタスク" in line or "Active Tasks" in line:
            lines.insert(i + 1, new_entry)
            inserted = True
            break
            
    if not inserted:
        lines.append(new_entry)

    with open(taskboard_path, "w", encoding="utf-8") as f:
        f.writelines(lines)
    print(f"🚀 TaskBoard updated: {taskboard_path}")

def complete_task(keyword, root_dir):
    taskboard_path = Path(root_dir) / "TaskBoard.md"
    if not taskboard_path.exists():
        return

    date_str = datetime.date.today().strftime("%Y-%m-%d")
    with open(taskboard_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    new_lines = []
    found = False
    for line in lines:
        if keyword in line and "[ ]" in line:
            line = line.replace("[ ]", "[x]")
            line = line.strip() + f" <!-- done: {date_str} -->\n"
            found = True
            print(f"✅ Marked as completed: {line.strip()}")
        new_lines.append(line)

    if found:
        with open(taskboard_path, "w", encoding="utf-8") as f:
            f.writelines(new_lines)
    else:
        print(f"❓ Task containing '{keyword}' not found or already completed.")

def archive_tasks(root_dir, days_threshold=3):
    taskboard_path = Path(root_dir) / "TaskBoard.md"
    archive_path = Path(root_dir) / ".agent" / "history" / "Task_Archive.md"
    if not taskboard_path.exists():
        return

    archive_path.parent.mkdir(parents=True, exist_ok=True)
    
    today = datetime.date.today()
    with open(taskboard_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    remaining_lines = []
    archived_lines = []
    
    for line in lines:
        match = re.search(r"<!-- done: (\d{4}-\d{2}-\d{2}) -->", line)
        if match:
            done_date = datetime.datetime.strptime(match.group(1), "%Y-%m-%d").date()
            if (today - done_date).days >= days_threshold:
                archived_lines.append(line)
                continue
        remaining_lines.append(line)

    if archived_lines:
        # Append to archive
        with open(archive_path, "a", encoding="utf-8") as f:
            if f.tell() == 0:
                f.write("# 📦 Task Archive\n\n")
            f.writelines(archived_lines)
        
        # Write back to taskboard
        with open(taskboard_path, "w", encoding="utf-8") as f:
            f.writelines(remaining_lines)
        print(f"📁 Archived {len(archived_lines)} tasks to {archive_path}")
    else:
        print("✨ No tasks to archive.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command")

    # Create command
    create_parser = subparsers.add_parser("create")
    create_parser.add_argument("title", help="Title of the task")
    create_parser.add_argument("--priority", default="Medium", help="Priority (High/Medium/Low)")
    create_parser.add_argument("--simple", action="store_true", help="If set, don't create a detailed file")
    create_parser.add_argument("--root", default=".", help="Project root directory")

    # Complete command
    complete_parser = subparsers.add_parser("complete")
    complete_parser.add_argument("keyword", help="Keyword to identify the task")
    complete_parser.add_argument("--root", default=".", help="Project root directory")

    # Archive command
    archive_parser = subparsers.add_parser("archive")
    archive_parser.add_argument("--days", type=int, default=3, help="Days threshold for archiving")
    archive_parser.add_argument("--root", default=".", help="Project root directory")

    args = parser.parse_args()
    root_abs = os.path.abspath(args.root if args.root else ".")

    if args.command == "create":
        create_task(args.title, args.priority, root_abs, not args.simple)
    elif args.command == "complete":
        complete_task(args.keyword, root_abs)
    elif args.command == "archive":
        archive_tasks(root_abs, args.days)
