import os
import json
import argparse
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
            # Lookup
            if props.get("lookup"):
                related_app = props["lookup"].get("relatedApp", {}).get("app")
                if related_app:
                    links.append({
                        "from": app_id,
                        "to": related_app,
                        "type": "Lookup",
                        "field": code,
                        "label": props.get("label")
                    })
            
            # Related Records
            if props.get("type") == "REFERENCE_TABLE":
                related_app = props.get("referenceTable", {}).get("relatedApp", {}).get("app")
                if related_app:
                    links.append({
                        "from": app_id,
                        "to": related_app,
                        "type": "RelatedRecord",
                        "field": code,
                        "label": props.get("label")
                    })

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
                links.append({
                    "from": app_id,
                    "to": dest_app,
                    "type": "AppAction",
                    "name": action_name
                })

    return links, app_names

def main():
    parser = argparse.ArgumentParser(description='Analyze links between kintone apps for Mermaid.')
    parser.add_argument('--input', required=True, help='Directory containing fetched JSONs')
    parser.add_argument('--output', default='links_summary.md', help='Output Mermaid/Markdown file')
    args = parser.parse_args()

    links, app_names = analyze_links(args.input)
    
    # Deduplicate and Clean
    seen_links = set()
    unique_links = []
    for link in links:
        # Clean up labels and names for Mermaid
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
        f.write("# Kintone App Links Analysis\n\n")
        f.write("## Mermaid Flowchart (Draft)\n\n")
        f.write("```mermaid\ngraph RL\n") # Original RL layout
        
        # Define nodes with names
        sorted_apps = sorted(app_names.items(), key=lambda x: int(x[0]) if x[0].isdigit() else 99999)
        for app_id, name in sorted_apps:
            # Clean app name
            clean_name = str(name).replace('\n', ' ').replace('"', "'").strip()
            f.write(f'  app_{app_id}["{app_id}: {clean_name}"]\n')

        for link in links:
            from_id = link['from']
            to_id = link['to']
            if link['type'] == 'Lookup':
                f.write(f"  app_{from_id} -- |Lookup: {link['field']}| --> app_{to_id}\n")
            elif link['type'] == 'RelatedRecord':
                f.write(f"  app_{from_id} -. |Rel: {link['field']}| .-> app_{to_id}\n")
            elif link['type'] == 'AppAction':
                f.write(f"  app_{from_id} ==> |Action: {link['name']}| app_{to_id}\n")
        
        f.write("```\n\n")
        f.write("## Details\n\n")
        f.write("| From App | To App | Type | Detail |\n")
        f.write("|---|---|---|---|\n")
        for link in links:
            from_name = app_names.get(link['from'], "Unknown")
            to_name = app_names.get(link['to'], "Unknown")
            detail = link.get('label') or link.get('name') or link.get('field')
            f.write(f"| {link['from']}: {from_name} | {link['to']}: {to_name} | {link['type']} | {detail} |\n")

    print(f"Analysis complete! Results saved to: {args.output}")

if __name__ == "__main__":
    main()
