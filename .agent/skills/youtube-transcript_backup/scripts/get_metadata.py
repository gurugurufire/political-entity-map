#!/usr/bin/env python3
import yt_dlp
import json
import sys
import argparse

def get_video_info(url):
    ydl_opts = {
        'quiet': True,
        'skip_download': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=False)
            result = {
                'channel': info.get('uploader'),
                'channel_url': info.get('uploader_url'),
                'title': info.get('title'),
                'upload_date': info.get('upload_date'),
                'view_count': info.get('view_count'),
                'tags': info.get('tags'),
                'description': info.get('description'),
                'webpage_url': info.get('webpage_url')
            }
            return result
        except Exception as e:
            return {'error': str(e)}

def main():
    parser = argparse.ArgumentParser(description='Get metadata from a YouTube video')
    parser.add_argument('url', help='The URL of the YouTube video')
    parser.add_argument('--output', '-o', help='Output JSON file path')

    args = parser.parse_args()
    info = get_video_info(args.url)
    
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(info, f, ensure_ascii=False, indent=2)
        print(f"Metadata saved to: {args.output}")
    else:
        # For terminal output, we need to be careful with encoding on Windows
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except:
            pass
        print(json.dumps(info, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
