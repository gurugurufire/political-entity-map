import re
import yaml
from pathlib import Path
from datetime import datetime

# CONFIGURATION
# .agent はマッピング対象として重要なので除外しない
IGNORE_DIRS = {'.git', '.vscode', '__pycache__', 'node_modules', 'venv', '.venv', 'tmp', 'backups'} 
IGNORE_FILES = {'TaskBoard.md', 'AgentGuide.md', 'AgentHistory.md', 'PROJECT_MAP.md', '.DS_Store', 'Thumbs.db'}

def get_file_info(file_path):
    """タイトル(H1)と最終更新日を取得"""
    title = file_path.name
    description = ""
    try:
        content = file_path.read_text(encoding='utf-8')
        # H1 Title
        match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        if match:
            title = match.group(1).strip()
        
        # YAML Description (for Workflows/Skills)
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                try:
                    meta = yaml.safe_load(parts[1])
                    if 'description' in meta:
                        description = meta['description']
                    elif 'name' in meta:
                        title = meta['name']
                except:
                    pass
    except Exception:
        pass
    
    mtime = datetime.fromtimestamp(file_path.stat().st_mtime).strftime('%Y-%m-%d')
    return title, mtime, file_path.name, description

def generate_skills_readme(skills_dir):
    """.agent/skills/README.md を生成"""
    content = ["# 🛠️ Agent Skills\n\n"]
    content.append("エージェントの専門技能（Skills）の目次です。\n\n")
    content.append("| スキル名 | 説明 | 最終更新 |\n")
    content.append("| :--- | :--- | :--- |\n")
    
    for skill_path in sorted(skills_dir.iterdir()):
        if skill_path.is_dir() and (skill_path / "SKILL.md").exists():
            title, mtime, _, desc = get_file_info(skill_path / "SKILL.md")
            link = f"[{title}](skills/{skill_path.name}/SKILL.md)"
            content.append(f"| {link} | {desc} | {mtime} |\n")
            
    readme_path = skills_dir.parent / "Skill_Index.md"
    readme_path.write_text("".join(content), encoding='utf-8')
    print(f"✅ Updated {readme_path}")

def generate_workflows_readme(workflows_dir):
    """.agent/workflows/README.md を生成"""
    content = ["# 🔄 Agent Workflows\n\n"]
    content.append("定型作業を自動化・標準化するための「手順書」です。\n\n")
    content.append("| ワークフロー | 目的 | 最終更新 |\n")
    content.append("| :--- | :--- | :--- |\n")
    
    for wf_path in sorted(workflows_dir.iterdir()):
        if wf_path.suffix == '.md' and wf_path.name != 'README.md':
            title, mtime, filename, desc = get_file_info(wf_path)
            # Remove extension for display title if it's just the filename
            display_title = title if title != filename else filename.replace('.md', '')
            link = f"[{display_title}](workflows/{filename})"
            content.append(f"| {link} | {desc} | {mtime} |\n")
            
    readme_path = workflows_dir.parent / "Workflow_Index.md"
    readme_path.write_text("".join(content), encoding='utf-8')
    print(f"✅ Updated {readme_path}")

def generate_markdown_tree(root_dir):
    """プロジェクトマップ全体を日本語で生成"""
    
    content = ["# 🗺️ Project Map (プロジェクト全土地図)\n"]
    content.append(f"> **最終更新**: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
    content.append("> この地図は `project-caretaker` スキルによって自動生成されました。\n\n")

    # マッピング対象のセクション定義 (タイトル, パス)
    sections = [
        ("📂 公式ドキュメント (docs/)", "docs"),
        ("🛠️ スクリプト・ツール (scripts/)", "scripts"),
        ("⚡ ソースコード (src/)", "src"),
        ("🤖 エージェント脳内 (.agent/)", ".agent"), # .agent 全体を表示
        ("📜 ルートファイル", ".")
    ]

    for section_title, dir_name in sections:
        content.append(f"## {section_title}\n")
        content.append("| 更新日 | ファイル名 | 説明 (タイトル) |\n")
        content.append("|---|---|---|\n")
        
        target_path = root_dir / dir_name
        files = []
        
        if dir_name == ".":
            # ルート直下のみ
            files = [f for f in root_dir.iterdir() if f.is_file() and f.name not in IGNORE_FILES]
        elif target_path.exists():
             # 再帰的に取得
             files = sorted(target_path.rglob('*'))
        
        # 行データの生成
        rows = []
        for file in files:
             if file.is_dir(): continue
             
             # 無視リストチェック
             # パスの一部に IGNORE_DIRS が含まれているか（ただしターゲット自体が .agent の場合はルート直下の .agent は許容したいが、中の tmp とかは除外したい）
             is_ignored = False
             for part in file.parts:
                 if part in IGNORE_DIRS:
                     is_ignored = True
                     break
             if is_ignored: continue

             if file.name in IGNORE_FILES: continue
             if dir_name == "." and file.name.startswith('.'): continue
             if file.name == 'PROJECT_MAP.md': continue

             title, date, filename, description = get_file_info(file)
             
             # リンク用相対パス
             try:
                 rel_path = file.relative_to(root_dir).as_posix()
                 link = f"[{filename}]({rel_path})"
             except:
                 link = filename
             
             # ファイル名とタイトルが同じなら説明を空にする、YAMLの説明があればそれを優先
             desc = description if description else (title if title != filename else "")
             
             rows.append(f"| {date} | {link} | {desc} |\n")
        
        if rows:
            content.extend(rows)
        else:
            content.append("| - | *ファイルなし* | - |\n")
        
        content.append("\n\n")

    return "".join(content)

if __name__ == "__main__":
    root = Path.cwd().resolve()
    
    # Generate Local READMEs
    skills_dir = root / ".agent" / "skills"
    if skills_dir.exists():
        generate_skills_readme(skills_dir)
        
    workflows_dir = root / ".agent" / "workflows"
    if workflows_dir.exists():
        generate_workflows_readme(workflows_dir)
        
    # Generate Global Map
    target_file = root / "PROJECT_MAP.md"
    print(f"🗺️ Generating Project Map at: {target_file}...")
    markdown_content = generate_markdown_tree(root)
    
    target_file.write_text(markdown_content, encoding='utf-8')
    print("✨ Project Map updated successfully!")
