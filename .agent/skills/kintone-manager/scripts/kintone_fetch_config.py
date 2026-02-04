import os
import json
import requests
import argparse
import csv
from datetime import datetime
from dotenv import load_dotenv

class KintoneFetcher:
    def __init__(self, base_url, username=None, password=None, api_tokens=None):
        self.base_url = base_url.rstrip('/')
        self.headers = {
            'X-Cybozu-Authorization': None, # To be filled if using password
            'X-Cybozu-API-Token': api_tokens # Comma separated tokens
        }
        if username and password:
            import base64
            auth_str = f"{username}:{password}"
            encoded_auth = base64.b64encode(auth_str.encode('utf-8')).decode('utf-8')
            self.headers['X-Cybozu-Authorization'] = encoded_auth
            
    def _get(self, endpoint, params):
        url = f"{self.base_url}/k/v1/{endpoint}"
        resp = requests.get(url, params=params, headers={k: v for k, v in self.headers.items() if v is not None})
        resp.raise_for_status()
        return resp.json()

    def fetch_app_info(self, app_id):
        print(f"Fetching config for App ID: {app_id}...")
        
        # 1. Fields
        fields = self._get("app/form/fields.json", {"app": app_id})
        
        # 2. Layout
        layout = self._get("app/form/layout.json", {"app": app_id})
        
        # 3. Actions
        actions = self._get("app/actions.json", {"app": app_id})

        # 4. Settings (to get App Name)
        settings = self._get("app/settings.json", {"app": app_id})
        
        return {
            "fields": fields.get("properties", {}),
            "layout": layout.get("layout", []),
            "actions": actions.get("actions", {}),
            "settings": settings
        }

    def merge_and_flatten(self, layout, properties):
        """Logic reconstructed from src/desktop.js"""
        def process_layout(layout_items, path=[], group=None, table=None, row_idx=None):
            rows = []
            for idx, item in enumerate(layout_items):
                current_row_idx = row_idx if row_idx is not None else idx
                
                if item['type'] == 'ROW':
                    for f_idx, field in enumerate(item.get('fields', [])):
                        if field['type'] == 'GROUP':
                            rows.extend(process_layout(field['layout'], path + [f"GROUP:{field['code']}"], group=field['code'], table=table, row_idx=current_row_idx))
                        elif field['type'] == 'SUBTABLE':
                            # Subtable fields are processed as children
                            rows.extend(process_layout(field['fields'], path + [f"SUBTABLE:{field['code']}"], group=group, table=field['code'], row_idx=current_row_idx))
                        else:
                            field_code = field.get('code')
                            merged_field = {**field, **properties.get(field_code, {})}
                            merged_field.update({
                                "_rowIndex": current_row_idx,
                                "_childIndex": f_idx,
                                "_groupCode": group,
                                "_tableCode": table,
                                "_layoutPath": " > ".join(path)
                            })
                            rows.append(merged_field)
                elif item['type'] == 'GROUP':
                    rows.extend(process_layout(item['layout'], path + [f"GROUP:{item['code']}"], group=item['code'], table=table, row_idx=row_idx))
                elif item['type'] == 'SUBTABLE':
                    # Special handling for subtable fields array
                    for f_idx, sub_field in enumerate(item.get('fields', [])):
                        field_code = sub_field.get('code')
                        merged_field = {**sub_field, **properties.get(field_code, {})}
                        merged_field.update({
                            "_rowIndex": current_row_idx,
                            "_childIndex": f_idx,
                            "_groupCode": group,
                            "_tableCode": item['code'],
                            "_layoutPath": " > ".join(path + [f"SUBTABLE:{item['code']}"])
                        })
                        rows.append(merged_field)
            return rows

        return process_layout(layout)

def main():
    parser = argparse.ArgumentParser(description='Fetch kintone app configuration.')
    parser.add_argument('--app', required=True, help='App ID')
    parser.add_argument('--output', default='./output', help='Output directory')
    parser.add_argument('--token', help='API Token')
    args = parser.parse_args()

    # Explicitly look for .env in the current working directory
    dotenv_path = os.path.join(os.getcwd(), '.env')
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)
    else:
        load_dotenv() # fallback
    
    print(f"DEBUG: CWD={os.getcwd()}")
    print(f"DEBUG: dotenv_path={dotenv_path} (exists: {os.path.exists(dotenv_path)})")
    base_url = os.getenv('KINTONE_BASE_URL')
    if not base_url and os.getenv('KINTONE_DOMAIN'):
        base_url = f"https://{os.getenv('KINTONE_DOMAIN')}.cybozu.com"
        
    username = os.getenv('KINTONE_USERNAME') or os.getenv('KINTONE_ID')
    password = os.getenv('KINTONE_PASSWORD') or os.getenv('KINTONE_PASS')

    print(f"DEBUG: base_url={base_url}, username={username}, password={'***' if password else 'None'}")

    if not base_url or not username or not password:
        print("Error: Missing kintone credentials in .env file.")
        print("Required: KINTONE_BASE_URL (or KINTONE_DOMAIN), KINTONE_USERNAME (or KINTONE_ID), KINTONE_PASSWORD (or KINTONE_PASS)")
        return
    
    fetcher = KintoneFetcher(base_url, username, password, args.token)
    
    try:
        data = fetcher.fetch_app_info(args.app)
        
        # Create output dir
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        target_dir = os.path.join(args.output, f"app_{args.app}_{timestamp}")
        os.makedirs(target_dir, exist_ok=True)
        
        # Save raw JSONs
        with open(os.path.join(target_dir, "raw_fields.json"), "w", encoding="utf-8") as f:
            json.dump(data['fields'], f, indent=2, ensure_ascii=False)
        with open(os.path.join(target_dir, "raw_actions.json"), "w", encoding="utf-8") as f:
            json.dump(data['actions'], f, indent=2, ensure_ascii=False)
        with open(os.path.join(target_dir, "raw_settings.json"), "w", encoding="utf-8") as f:
            json.dump(data['settings'], f, indent=2, ensure_ascii=False)
            
        # Flatten and save CSV
        flattened = fetcher.merge_and_flatten(data['layout'], data['fields'])
        if flattened:
            keys = set()
            for row in flattened:
                keys.update(row.keys())
            
            # Sort keys: metadata first, then alphabet
            preferred = ["label", "code", "type", "_rowIndex", "_childIndex", "_groupCode", "_tableCode", "_layoutPath", "lookup"]
            header = [k for k in preferred if k in keys] + sorted([k for k in keys if k not in preferred])
            
            csv_path = os.path.join(target_dir, f"form_definition_{args.app}.csv")
            with open(csv_path, "w", encoding="utf-8-sig", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=header)
                writer.writeheader()
                for row in flattened:
                    # Clean up dict for writer
                    filtered_row = {k: v for k, v in row.items() if k in header}
                    writer.writerow(filtered_row)
            
            print(f"Success! Data saved to: {target_dir}")
        else:
            print("No fields found.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
