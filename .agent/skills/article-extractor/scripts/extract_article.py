#!/usr/bin/env python3
import sys
import argparse
import os
from urllib.request import Request, urlopen
from urllib.error import URLError

try:
    import trafilatura
    TRAFILATURA_AVAILABLE = True
except ImportError:
    TRAFILATURA_AVAILABLE = False

try:
    from bs4 import BeautifulSoup
    BS4_AVAILABLE = True
except ImportError:
    BS4_AVAILABLE = False

def extract_with_trafilatura(url, output_format='txt'):
    downloaded = trafilatura.fetch_url(url)
    if not downloaded:
        return None
    return trafilatura.extract(downloaded, output_format=output_format, include_comments=False, include_tables=True)

def extract_with_bs4(url):
    try:
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urlopen(req) as response:
            html = response.read().decode('utf-8', errors='ignore')
        
        soup = BeautifulSoup(html, 'html.parser')
        
        # Remove noisy elements
        for element in soup(['script', 'style', 'nav', 'header', 'footer', 'aside', 'form']):
            element.decompose()
            
        # Try to find main content
        main_content = soup.find('main') or soup.find('article') or soup.find('div', class_=lambda x: x and ('content' in x.lower() or 'article' in x.lower()))
        
        if main_content:
            return main_content.get_text(separator='\n\n').strip()
        else:
            return soup.get_text(separator='\n\n').strip()
    except Exception as e:
        print(f"Error in BS4 extraction: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description='Extract article content from a URL')
    parser.add_argument('url', help='The URL of the article')
    parser.add_argument('--output', '-o', help='Output file path')
    parser.add_argument('--format', '-f', choices=['txt', 'md', 'xml', 'json'], default='txt', help='Output format')

    args = parser.parse_args()

    print(f"Extracting content from: {args.url}")
    
    content = None
    if TRAFILATURA_AVAILABLE:
        print("Using trafilatura for extraction...")
        content = extract_with_trafilatura(args.url, output_format=args.format if args.format != 'md' else 'txt')
    elif BS4_AVAILABLE:
        print("Trafilatura not found. Using BeautifulSoup for fallback extraction...")
        content = extract_with_bs4(args.url)
    else:
        print("No advanced extraction libraries found. Using basic URL read...")
        try:
            req = Request(args.url, headers={'User-Agent': 'Mozilla/5.0'})
            with urlopen(req) as response:
                content = response.read().decode('utf-8', errors='ignore')
                # This will be raw HTML, which isn't great.
        except Exception as e:
            print(f"Error: {e}")

    if content:
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Content saved to: {args.output}")
        else:
            print("\n--- EXTRACTED CONTENT ---\n")
            print(content)
            print("\n-------------------------\n")
    else:
        print("Failed to extract content.")
        sys.exit(1)

if __name__ == "__main__":
    main()
