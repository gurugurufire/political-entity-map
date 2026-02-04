import os
import shutil
import json
import argparse
from pathlib import Path
from datetime import datetime

def load_rules(rules_path):
    with open(rules_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def should_ignore(file_path, rules):
    name = file_path.name
    if name in rules.get("ignore_files", []):
        return True
    return False

def get_destination(file_path, rules):
    name = file_path.name
    ext = file_path.suffix.lower()

    for rule in rules.get("rules", []):
        # API Check: "prefixes"
        if "prefixes" in rule:
            for prefix in rule["prefixes"]:
                if name.startswith(prefix):
                    return rule["destination"]
        
        # API Check: "extensions"
        if "extensions" in rule:
            if ext in rule["extensions"]:
                return rule["destination"]
    
    return None

def create_backup(file_path, backup_root):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = Path(backup_root) / f"backup_{timestamp}"
    backup_dir.mkdir(parents=True, exist_ok=True)
    
    shutil.copy2(file_path, backup_dir / file_path.name)
    return backup_dir

def organize(root_path, rules_path, dry_run=False):
    rules = load_rules(rules_path)
    root = Path(root_path)
    
    # Load ignore dirs/files
    ignore_dirs = set(rules.get("ignore_dirs", []))
    
    print(f"🧹 Organizing {root}...")
    
    # Identify files to move first
    files_to_move = []
    for item in root.iterdir():
        if item.is_dir():
            continue
        if should_ignore(item, rules):
            continue
        
        dest_rel = get_destination(item, rules)
        if dest_rel:
             files_to_move.append((item, dest_rel))
    
    if not files_to_move:
        print("✨ No files to organize.")
        return

    if dry_run:
        print("🔍 DRY RUN MODE: No files will be moved.")
        for item, dest_rel in files_to_move:
             print(f"  [PLAN] Move: {item.name} -> {dest_rel}/{item.name}")
        print(f"✨ Plan completed. {len(files_to_move)} files would be moved.")
        return

    # Backup Phase
    backup_root = root / ".agent/tmp/backups"
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    current_backup_dir = backup_root / f"run_{timestamp}"
    current_backup_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"📦 Creating backup in: {current_backup_dir}")
    try:
        for item, _ in files_to_move:
            shutil.copy2(item, current_backup_dir / item.name)
        print("✅ Backup completed successfully.")
    except Exception as e:
        print(f"❌ Backup failed: {e}")
        print("🛑 Aborting organization to prevent data loss.")
        return

    # Move Phase
    moved_count = 0
    for item, dest_rel in files_to_move:
        dest_dir = root / dest_rel
        dest_path = dest_dir / item.name
        
        # Ensure dest dir exists
        dest_dir.mkdir(parents=True, exist_ok=True)
        
        # Handle collision
        if dest_path.exists():
            print(f"  [SKIP] Destination exists: {dest_path}")
            continue
        
        try:
            shutil.move(str(item), str(dest_path))
            print(f"  [MOVE] {item.name} -> {dest_rel}/{item.name}")
            moved_count += 1
        except Exception as e:
             print(f"  [ERROR] Failed to move {item.name}: {e}")

    print(f"✨ Organization completed. {moved_count} files moved.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Organize project files based on rules.")
    parser.add_argument("--root", default=".", help="Project root directory")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be done without doing it")
    
    args = parser.parse_args()
    
    # Resolve paths
    current_file = Path(__file__).resolve()
    skill_dir = current_file.parent.parent
    resources_dir = skill_dir / "resources"
    rules_file = resources_dir / "mapping_rules.json"
    
    # If looking from execution context (cwd)
    root_dir = Path(os.getcwd()).resolve()
    
    if not rules_file.exists():
        print(f"❌ Error: Rules file not found at {rules_file}")
        exit(1)
        
    organize(root_dir, rules_file, args.dry_run)
