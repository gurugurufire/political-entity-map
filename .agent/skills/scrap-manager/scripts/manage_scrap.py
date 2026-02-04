import os
import datetime
import argparse
from pathlib import Path

def create_scrap(title, category, root_dir, url=None):
    date_str = datetime.date.today().strftime("%Y-%m-%d")
    safe_title = title.replace(" ", "_").replace("/", "-")
    filename = f"{date_str}-{safe_title}.md"
    
    # Paths
    scraps_dir = Path(root_dir) / "docs" / "research" / "scraps"
    dashboard_path = Path(root_dir) / "docs" / "research" / "Discovery_Log.md"
    
    scraps_dir.mkdir(parents=True, exist_ok=True)
    scrap_path = scraps_dir / filename
    
    # Create the detailed scrap file
    url_section = f"- **URL**: {url}" if url else "- **URL**: (None)"
    content = f"""# 📝 {title}
- **Date**: {date_str}
- **Category**: {category}
{url_section}

## 🔍 Overview
(ここに詳細を記述してください)

## 🔗 References
- {url if url else ''}

---
Created by scrap-manager skill
"""
    if not scrap_path.exists():
        with open(scrap_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"✅ Created scrap: {scrap_path}")
    else:
        print(f"⚠️ Scrap already exists: {scrap_path}")

    # Update Dashboard
    update_dashboard(title, category, f"scraps/{filename}", dashboard_path)

def update_dashboard(title, category, rel_path, dashboard_path):
    date_str = datetime.date.today().strftime("%Y-%m-%d")
    entry = f"- [{date_str}] [{category}] [{title}]({rel_path})\n"
    
    if not dashboard_path.exists():
        header = "# 📒 Discovery Log (Dashboard)\n\n"
        with open(dashboard_path, "w", encoding="utf-8") as f:
            f.write(header)

    with open(dashboard_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Insert at the top of the list (usually after the first header)
    insert_pos = 0
    for i, line in enumerate(lines):
        if line.startswith("# ") or line.startswith("---"):
            continue
        if line.strip() == "":
            continue
        insert_pos = i
        break
    else:
        insert_pos = len(lines)

    lines.insert(insert_pos, entry)
    
    with open(dashboard_path, "w", encoding="utf-8") as f:
        f.writelines(lines)
    print(f"🚀 Dashboard updated: {dashboard_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("title", help="Title of the scrap")
    parser.add_argument("--category", default="General", help="Category of the scrap")
    parser.add_argument("--url", help="Source URL of the scrap")
    parser.add_argument("--root", default=".", help="Project root directory")
    args = parser.parse_args()
    
    # Use absolute path if provided root is '.'
    root_abs = os.path.abspath(args.root)
    create_scrap(args.title, args.category, root_abs, args.url)
