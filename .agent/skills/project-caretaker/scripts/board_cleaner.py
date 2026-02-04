import re
import argparse
from datetime import datetime
from pathlib import Path

def get_current_date_str():
    return datetime.now().strftime("%Y-%m-%d")

def clean_board(file_path, dry_run=False):
    path = Path(file_path)
    if not path.exists():
        print(f"❌ File not found: {path}")
        return

    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    new_lines = []
    completed_tasks = []
    
    # State
    buffer_task = [] # List of lines for current task
    is_buffer_completed = False
    in_completed_section = False
    
    # Regex
    task_start_pattern = re.compile(r'^(\s*)-\s*\[([ x])\]') # Matches "- [ ]" or "- [x]" with indentation
    header_pattern = re.compile(r'^#{2,}\s+')
    completed_header_pattern = re.compile(r'^#{2,}\s+.*(完了|Completed|Done|Archives).*', re.IGNORECASE)

    def flush_buffer():
        nonlocal buffer_task, is_buffer_completed
        if not buffer_task:
            return
        
        # Ensure completion date is added if missing
        if is_buffer_completed:
            first_line = buffer_task[0]
            if "<!-- done:" not in first_line:
                # Add date
                buffer_task[0] = first_line.rstrip() + f" <!-- done: {get_current_date_str()} -->\n"
            
            completed_tasks.extend(buffer_task)
        else:
            new_lines.extend(buffer_task)
        
        buffer_task = []
        is_buffer_completed = False

    for line in lines:
        # Check for Section Headers
        if header_pattern.match(line):
            flush_buffer() # Finish pending task processing
            
            new_lines.append(line)
            
            if completed_header_pattern.match(line):
                in_completed_section = True
            else:
                in_completed_section = False
            continue
        
        # If we are already in the Completed section, just keep everything as is (or maybe we skip them to re-append? No, keep structure)
        # Actually to "Archive", we might want to capture them too if we want to sort?
        # For now, let's assume we LEAVE existing completed items where they are, and just APPEND new ones.
        if in_completed_section:
            flush_buffer()
            new_lines.append(line)
            continue

        # Check for Task Start
        match = task_start_pattern.match(line)
        if match:
            # It's a task.
            flush_buffer() # Flush previous
            
            indent = match.group(1)
            status = match.group(2) # ' ' or 'x'
            
            # Only treat top-level tasks (no indentation or small indentation?)
            # Usually we only move Top Level tasks.
            # If a sub-task is done but parent is not, we generally DON'T move it out of context.
            # So, we only consider tasks with NO indentation or specific bullet indentation as "Movable".
            # For simplicity: Only move active tasks if they are checked.
            
            # IMPORTANT: If indentation > 0, it might be a subtask.
            # We only move tasks if the PARENT is done.
            # Impl: If a line starts a task:
            # We assume it's a new block.
            # Wait, if it is a subtask, it should be part of the `buffer_task` of the parent.
            # Logic Update:
            # If match and indent length is same as current buffer's indent... logic gets complex.
            # Simplified Logic:
            # A "Task Block" starts with "- [ ]" at indentation 0 (or standard list indent).
            # Anything following that is indented more is part of it.
            
            if len(indent) == 0 or indent == "": # Top level task
                buffer_task.append(line)
                if status == 'x':
                    is_buffer_completed = True
                else:
                    is_buffer_completed = False
            else:
                # Indented task (Subtask)
                # If we have a buffer, append to it (it belongs to parent)
                if buffer_task:
                    buffer_task.append(line)
                    # If parent was completed, this subtask goes with it.
                    # If parent was NOT completed, this subtask stays with it (even if subtask is [x])
                else:
                    # Orphaned subtask? Just treat as line
                    new_lines.append(line)
        else:
            # Not a task start (Note, description, empty line)
            # If we have a buffer, append to it
            if buffer_task:
                buffer_task.append(line)
            else:
                new_lines.append(line)
    
    flush_buffer()
    
    # now we have new_lines (without recently completed tasks) and completed_tasks (newly completed)
    # We need to inject completed_tasks into the "Completed" section.
    
    final_output = []
    in_comp = False
    inserted = False
    
    # Try to find the Completed section to insert
    processed_lines = new_lines
    
    # If no completed tasks to move, just return
    if not completed_tasks:
        print("✨ No new completed tasks found to archive.")
        return

    # Reconstruct file
    # We look for the "## ✅ 完了済み" header in processed_lines
    header_found = False
    for line in processed_lines:
        final_output.append(line)
        if completed_header_pattern.match(line):
            header_found = True
            # Insert our moved tasks here
            final_output.extend(completed_tasks)
            inserted = True
            
    if not header_found:
        # Append to end
        final_output.append("\n## ✅ 完了済み\n")
        final_output.extend(completed_tasks)
        inserted = True
        
    if dry_run:
        print(f"🔍 DRY RUN: Would archive {len([l for l in completed_tasks if '- [x]' in l])} tasks.")
        # print("--- Preview ---")
        # print("".join(final_output))
    else:
        with open(path, 'w', encoding='utf-8') as f:
            f.writelines(final_output)
        print(f"✨ Archived {len([l for l in completed_tasks if '- [x]' in l])} tasks to 'Completed' section.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", default="TaskBoard.md", help="Target TaskBoard file")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    
    # Find TaskBoard
    target_path = Path(args.target).resolve()
    if not target_path.exists():
        # Try finding in root if script run from elsewhere
        root_path = Path(os.getcwd()).resolve()
        target_path = root_path / "TaskBoard.md"
        
    clean_board(target_path, args.dry_run)
