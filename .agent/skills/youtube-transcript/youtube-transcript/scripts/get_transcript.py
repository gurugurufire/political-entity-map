#!/usr/bin/env python3
import sys
import argparse
import re
from youtube_transcript_api import YouTubeTranscriptApi

def get_video_id(url):
    # Extract video ID from various YouTube URL formats
    pattern = r'(?:v=|\/)([0-9A-Za-z_-]{11}).*'
    match = re.search(pattern, url)
    return match.group(1) if match else url

def main():
    parser = argparse.ArgumentParser(description='Get transcript from a YouTube video')
    parser.add_argument('url', help='The URL or video ID of the YouTube video')
    parser.add_argument('--output', '-o', help='Output file path')
    parser.add_argument('--languages', '-l', nargs='+', default=['ja', 'en'], help='Preferred languages (e.g., ja en)')

    args = parser.parse_args()
    video_id = get_video_id(args.url)

    print(f"Fetching transcript for video ID: {video_id}...")

    try:
        # Fetch the transcript
        api = YouTubeTranscriptApi()
        transcript_list = api.list(video_id)
        
        # Try to find the transcript in preferred languages
        transcript = transcript_list.find_transcript(args.languages)
        
        data = transcript.fetch()
        
        # Format the transcript
        full_text = " ".join([item.text for item in data])
        
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(full_text)
            print(f"Transcript saved to: {args.output}")
        else:
            print("\n--- TRANSCRIPT ---\n")
            print(full_text)
            print("\n------------------\n")
            
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
