import os
import json
import re
from collections import defaultdict

def extract_metadata_from_md(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find JSON blocks inside the metadata section
    # Matches: ```json ... ``` inside a ## Mapping Metadata section (with optional emoji)
    # allowing for text in between header and code block
    pattern = r'## .*?Mapping Metadata.*?```json\s+(.*?)\s+```'
    match = re.search(pattern, content, re.IGNORECASE | re.DOTALL)
    
    if match:
        try:
            data = json.loads(match.group(1))
            print(f"DEBUG: Successfully extracted JSON used from {file_path}")
            return data
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON in {file_path}: {e}")
    else:
        print(f"DEBUG: No JSON match found in {file_path}")
    return None

def aggregate_data(data_dir, target_tag=None):
    entities_map = defaultdict(lambda: {"stances": [], "sentiments": [], "sources": []})
    sources_map = {} # Tracking unique source bias
    
    for filename in os.listdir(data_dir):
        if filename.endswith(".md"):
            meta = extract_metadata_from_md(os.path.join(data_dir, filename))
            if meta:
                # Tag filtering
                if target_tag:
                    project_tags = meta.get("project_tags", [])
                    print(f"DEBUG: Processing {filename}, Tags: {project_tags}, Target: {target_tag}")
                    if target_tag not in project_tags:
                        print(f"DEBUG: Skipped {filename} due to tag mismatch (Has: {project_tags})")
                        continue
                
                source_info = meta.get("source", {})
                source_name = source_info.get("channel", "Unknown")
                
                # Store source bias for the source map
                if source_name not in sources_map:
                    sources_map[source_name] = source_info.get("source_bias", {
                        "anti_ds": 0.0, "establishment": 0.0, "tone_optimism": 0.0
                    })

                for entity in meta.get("entities", []):
                    name = entity.get("name")
                    entities_map[name]["stances"].append(entity.get("stance"))
                    entities_map[name]["sentiments"].append(entity.get("sentiment"))
                    entities_map[name]["sources"].append(source_name)

    return entities_map, sources_map

def generate_report(entities_map, sources_map):
    lines = []
    lines.append("# 🗺️ Political Entity & Source Map (Aggregated)")
    lines.append(f"Generated on: {os.popen('date /t').read().strip()} {os.popen('time /t').read().strip()}")
    
    lines.append("\n## 👥 1. Entity Analysis (勢力図)")
    lines.append("| Entity | Avg. Sentiment | Mentions | Primary Stance(s) | Sources |")
    lines.append("| :--- | :---: | :---: | :--- | :--- |")
    
    entity_data = []
    max_mentions = 1
    
    for name, data in entities_map.items():
        avg_sent = sum(data["sentiments"]) / len(data["sentiments"])
        mentions = len(data["sentiments"])
        max_mentions = max(max_mentions, mentions)
        stances = ", ".join(set(data["stances"]))
        sources = ", ".join(set(data["sources"]))
        sentiment_emoji = "🔴" if avg_sent < -0.3 else "🟢" if avg_sent > 0.3 else "⚪"
        
        lines.append(f"| **{name}** | {sentiment_emoji} {avg_sent:.2f} | {mentions} | {stances} | {sources} |")
        entity_data.append({"name": name, "sentiment": avg_sent, "mentions": mentions})

    # Entity Quadrant Chart
    lines.append("\n### 🌀 Political Entity Landscape")
    lines.append("```mermaid")
    lines.append("quadrantChart")
    lines.append("    title \"Entity Sentiment vs Attention\"")
    lines.append("    x-axis \"Negative (-1.0)\" --> \"Positive (+1.0)\"")
    lines.append("    y-axis \"Low Attention\" --> \"High Attention\"")
    lines.append("    quadrant-1 \"🚀 Leading / Influential\"")
    lines.append("    quadrant-2 \"⚠️ High Profile / Critical\"")
    lines.append("    quadrant-3 \"🔍 Niche / Skeptical\"")
    lines.append("    quadrant-4 \"🌱 Emerging / Support\"")
    for item in entity_data:
        x = (item["sentiment"] + 1) / 2
        y = (item["mentions"] - 1) / (max_mentions - 1) * 0.8 + 0.1 if max_mentions > 1 else 0.5
        
        # Clamp values to avoid edge parsing errors
        x = max(0.02, min(0.98, x))
        y = max(0.02, min(0.98, y))
        
        lines.append(f"    \"{item['name']}\": [{x:.2f}, {y:.2f}]")
    lines.append("```")

    lines.append("\n## 🌐 2. Information Source Analysis (発信者マップ)")
    lines.append("| Source Channel | Anti-DS | Establishment | Tone (Optimism) |")
    lines.append("| :--- | :---: | :---: | :---: |")
    
    for s_name, bias in sources_map.items():
        opt_emoji = "☀️" if bias['tone_optimism'] > 0.3 else "⛈️" if bias['tone_optimism'] < -0.3 else "☁️"
        lines.append(f"| **{s_name}** | {bias['anti_ds']:.2f} | {bias['establishment']:.2f} | {opt_emoji} {bias['tone_optimism']:.2f} |")

    # Source Quadrant Chart
    lines.append("\n### 🌀 Source Bias Landscape")
    lines.append("```mermaid")
    lines.append("quadrantChart")
    lines.append("    title \"Source: Anti-DS vs Establishment\"")
    lines.append("    x-axis \"Globalist (DS)\" --> \"Anti-DS (Sovereign)\"")
    lines.append("    y-axis \"Alternative\" --> \"Mainstream\"")
    lines.append("    quadrant-1 \"🏢 Traditional Conservative\"")
    lines.append("    quadrant-2 \"🏛️ Mainstream Globalist\"")
    lines.append("    quadrant-3 \"🏴 Alternative / Dissident\"")
    lines.append("    quadrant-4 \"🔥 Radical Anti-DS\"")
    for s_name, bias in sources_map.items():
        x = (bias["anti_ds"] + 1) / 2
        y = (bias["establishment"] + 1) / 2
        
        # Clamp values
        x = max(0.02, min(0.98, x))
        y = max(0.02, min(0.98, y))
        
        lines.append(f"    \"{s_name}\": [{x:.2f}, {y:.2f}]")
    lines.append("```")
    
    return "\n".join(lines)

if __name__ == "__main__":
    data_folder = "d:/VSCode/政治ネタ収集/data"
    output_file = "d:/VSCode/政治ネタ収集/POLITICAL_MAP.md"
    
    results, sources = aggregate_data(data_folder, target_tag=None)
    report = generate_report(results, sources)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"Political map generated: {output_file}")
