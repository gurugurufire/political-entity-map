import os
import json
import argparse
import csv
from glob import glob

def analyze_links(input_dir):
    """
    Look for raw_fields.json and raw_actions.json in subdirectories of input_dir
    and extract Lookup, Related Records, and App Actions.
    Also collect app names from raw_settings.json.
    """
    field_files = glob(os.path.join(input_dir, "**/raw_fields.json"), recursive=True)
    action_files = glob(os.path.join(input_dir, "**/raw_actions.json"), recursive=True)
    settings_files = glob(os.path.join(input_dir, "**/raw_settings.json"), recursive=True)
    
    links = []
    app_names = {}

    # Collect App Names
    for s_path in settings_files:
        app_id_parts = os.path.basename(os.path.dirname(s_path)).split("_")
        if len(app_id_parts) >= 2:
            app_id = app_id_parts[1]
            with open(s_path, "r", encoding="utf-8") as f:
                settings = json.load(f)
                app_names[app_id] = settings.get("name", f"App {app_id}")
    
    # Process Fields (Lookup & Related Records)
    for f_path in field_files:
        app_id_parts = os.path.basename(os.path.dirname(f_path)).split("_")
        if len(app_id_parts) < 2: continue
        app_id = app_id_parts[1]
        with open(f_path, "r", encoding="utf-8") as f:
            fields = json.load(f)
            
        for code, props in fields.items():
            if props.get("lookup"):
                related_app = props["lookup"].get("relatedApp", {}).get("app")
                if related_app:
                    links.append({"from": app_id, "to": related_app, "type": "Lookup", "field": code, "label": props.get("label")})
            
            if props.get("type") == "REFERENCE_TABLE":
                related_app = props.get("referenceTable", {}).get("relatedApp", {}).get("app")
                if related_app:
                    links.append({"from": app_id, "to": related_app, "type": "RelatedRecord", "field": code, "label": props.get("label")})

    # Process Actions
    for f_path in action_files:
        app_id_parts = os.path.basename(os.path.dirname(f_path)).split("_")
        if len(app_id_parts) < 2: continue
        app_id = app_id_parts[1]
        with open(f_path, "r", encoding="utf-8") as f:
            actions = json.load(f)
            
        for action_name, props in actions.items():
            dest_app = props.get("destApp", {}).get("app")
            if dest_app:
                links.append({"from": app_id, "to": dest_app, "type": "AppAction", "name": action_name})

    return links, app_names

def main():
    parser = argparse.ArgumentParser(description='Generate a structured Mermaid diagram with subgraphs.')
    parser.add_argument('--input', required=True, help='Directory containing fetched JSONs')
    parser.add_argument('--output', required=True, help='Output Markdown file')
    parser.add_argument('--csv', required=True, help='CSV file with App categories')
    args = parser.parse_args()

    links, app_names = analyze_links(args.input)
    
    # Load Categories
    categories = {}
    with open(args.csv, mode='r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            app_id = row.get('ID')
            cat = row.get('アプリ分類')
            if app_id and cat:
                categories[app_id.strip()] = cat.strip()

    # Deduplicate and Clean
    seen_links = set()
    unique_links = []
    for link in links:
        for key in ['label', 'name', 'field']:
            if key in link and link[key]:
                val = str(link[key]).replace('\n', ' ').replace('\r', '').strip()
                val = val.replace('(', '（').replace(')', '）').replace('[', '［').replace(']', '］').replace('|', '/')
                link[key] = val
        
        link_str = json.dumps(link, sort_keys=True)
        if link_str not in seen_links:
            seen_links.add(link_str)
            unique_links.append(link)
    
    links = unique_links

    with open(args.output, "w", encoding="utf-8") as f:
        f.write("# Kintone App Link Visualization (Structured)\n\n")
        f.write("```mermaid\ngraph LR\n")
        
        grouped_apps = {}
        for app_id, name in app_names.items():
            cat = categories.get(app_id, "外部・未定義")
            if cat not in grouped_apps: grouped_apps[cat] = []
            grouped_apps[cat].append((app_id, name))

        # Define nodes within subgraphs
        for cat, apps in grouped_apps.items():
            # Sanitize category for ID (alphanumeric only)
            import re
            safe_cat_id = re.sub(r'[^a-zA-Z0-9]', '_', cat)
            if not safe_cat_id[0].isalpha(): safe_cat_id = "cat_" + safe_cat_id
            
            f.write(f'  subgraph {safe_cat_id} ["{cat}"]\n')
            for app_id, name in sorted(apps, key=lambda x: int(x[0]) if x[0].isdigit() else 999):
                clean_name = str(name).replace('\n', ' ').replace('"', "'").strip()
                if "マスタ" in cat:
                    f.write(f'    app_{app_id}[("{app_id}: {clean_name}")]\n')
                else:
                    f.write(f'    app_{app_id}["{app_id}: {clean_name}"]\n')
            f.write("  end\n")

        for link in links:
            if link['type'] == 'Lookup':
                f.write(f"  app_{link['from']} -- |Lookup| --> app_{link['to']}\n")
            elif link['type'] == 'RelatedRecord':
                f.write(f"  app_{link['from']} -. |Rel| .-> app_{link['to']}\n")
            elif link['type'] == 'AppAction':
                f.write(f"  app_{link['from']} ==> |Act| app_{link['to']}\n")
        
        f.write("```\n")

    print(f"Structured visualization complete: {args.output}")

if __name__ == "__main__":
    main()
