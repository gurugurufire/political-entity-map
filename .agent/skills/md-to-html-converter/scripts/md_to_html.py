import os
import re
import sys
import markdown
from markdown.extensions.codehilite import CodeHiliteExtension
from markdown.extensions.toc import TocExtension

# --- 設定 (Settings) ---
CSS_URL = "https://cdnjs.cloudflare.com/ajax/libs/github-markdown-css/5.2.0/github-markdown.min.css"
MERMAID_JS_URL = "https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs"
FAVICON_URL = "https://www.rakuraku-hanbai.jp/favicon.ico" # 楽々販売のアイコンを拝借

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <link rel="icon" href="{favicon_url}">
    <link rel="stylesheet" href="{css_url}">
    <style>
        body {{
            box-sizing: border-box;
            min-width: 200px;
            max-width: 980px;
            margin: 0 auto;
            padding: 45px;
            background-color: #f6f8fa;
        }}
        .markdown-body {{
            padding: 40px;
            background-color: #ffffff;
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
            border-radius: 8px;
        }}
        @media (max-width: 767px) {{
            body {{ padding: 15px; }}
            .markdown-body {{ padding: 20px; }}
        }}
        /* Mermaid Diagram Styling */
        .mermaid {{
            display: flex;
            justify-content: center;
            margin: 20px 0;
            background-color: white !important;
        }}
        /* TOC Sticky */
        .toc {{
            background: #f8f9fa;
            padding: 15px;
            border-radius: 5px;
            border: 1px solid #e1e4e8;
            margin-bottom: 20px;
        }}
        .toc ul {{ list-style-type: none; padding-left: 20px; }}
        /* Code highlight tweaks */
        pre {{ background-color: #f6f8fa !important; }}
    </style>
</head>
<body>
    <article class="markdown-body">
        {content}
    </article>

    <script type="module">
        import mermaid from '{mermaid_js_url}';
        mermaid.initialize({{ 
            startOnLoad: true, 
            theme: 'default',
            securityLevel: 'loose',
            fontFamily: 'Inter, "Noto Sans JP", sans-serif'
        }});
    </script>
</body>
</html>
"""

def md_to_html(md_path, root_dir=None):
    if not os.path.exists(md_path):
        print(f"Error: File not found: {md_path}")
        return

    with open(md_path, 'r', encoding='utf-8') as f:
        text = f.read()

    # --- Pre-processing Mermaid ---
    def repl_mermaid(match):
        code = match.group(1).strip()
        return f'<pre class="mermaid">{code}</pre>'
    
    text = re.sub(r'```mermaid\s+(.*?)\s+```', repl_mermaid, text, flags=re.DOTALL)

    # --- Pre-processing Links (.md -> .html) ---
    def repl_links(match):
        label = match.group(1)
        link = match.group(2)
        if "://" in link:
            return match.group(0)
        
        new_link = link.replace(".md", ".html")
        return f'[{label}]({new_link})'

    text = re.sub(r'\[([^\]]+)\]\(([^)]+\.md)\)', repl_links, text)

    # --- Markdown Conversion ---
    md = markdown.Markdown(extensions=[
        'extra',
        CodeHiliteExtension(linenums=False, guess_lang=True),
        TocExtension(baselevel=1, title="目次"),
        'fenced_code',
        'tables',
        'nl2br'
    ])
    
    html_content = md.convert(text)
    
    # --- Template Rendering ---
    title = os.path.basename(md_path).replace(".md", "")
    final_html = HTML_TEMPLATE.format(
        title=title,
        content=html_content,
        css_url=CSS_URL,
        mermaid_js_url=MERMAID_JS_URL,
        favicon_url=FAVICON_URL
    )

    # --- Output ---
    md_dir = os.path.dirname(md_path)
    md_filename = os.path.basename(md_path)
    
    if root_dir:
        # Maintain structure
        # md_path: "root/sub/file.md", root_dir: "root"
        # rel_path: "sub/file.md"
        rel_dir = os.path.relpath(md_dir, root_dir)
        output_root = f"{root_dir.rstrip('/\\\\')}_html"
        output_dir = os.path.join(output_root, rel_dir)
    else:
        # Sibling directory (legacy mode)
        output_dir = f"{md_dir}_html" if md_dir else "html_output"

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created directory: {output_dir}")

    # Copy images
    image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.gif']
    if md_dir:
        for file in os.listdir(md_dir):
            _, ext = os.path.splitext(file)
            if ext.lower() in image_extensions:
                src_image = os.path.join(md_dir, file)
                dst_image = os.path.join(output_dir, file)
                if not os.path.exists(dst_image) or os.path.getmtime(src_image) > os.path.getmtime(dst_image):
                    import shutil
                    shutil.copy2(src_image, dst_image)
                    print(f"Copied image: {file}")
    
    output_filename = md_filename.replace(".md", ".html")
    output_path = os.path.join(output_dir, output_filename)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(final_html)
    
    print(f"Successfully converted: {output_path}")

def batch_convert(directory):
    directory = os.path.abspath(directory)
    target_files = []
    for root, dirs, files in os.walk(directory):
        if "_html" in root:
            continue
        for file in files:
            if file.endswith(".md"):
                target_files.append(os.path.join(root, file))
    
    for md_path in target_files:
        md_to_html(md_path, root_dir=directory)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python md_to_html.py <file_or_directory>")
        sys.exit(1)

    target = sys.argv[1]
    
    if os.path.isdir(target):
        batch_convert(target)
    else:
        md_to_html(target)
