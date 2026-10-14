"""Capture public sources locally; vendor snapshots are excluded from Git.

Uses only Python's standard library. Run from the repository root.
"""
import argparse
import concurrent.futures
import csv
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import time
from datetime import datetime, timezone
import urllib.request

ROOT = Path(__file__).resolve().parents[1]

class TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.skip = 0
        self.parts = []
    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style', 'noscript'):
            self.skip += 1
        if tag in ('p', 'h1', 'h2', 'h3', 'h4', 'li', 'tr', 'br'):
            self.parts.append('\n')
    def handle_endtag(self, tag):
        if tag in ('script', 'style', 'noscript') and self.skip:
            self.skip -= 1
        if tag in ('p', 'h1', 'h2', 'h3', 'h4', 'li', 'tr'):
            self.parts.append('\n')
    def handle_data(self, data):
        if not self.skip:
            self.parts.append(data)
    def text(self):
        return '\n'.join(' '.join(line.split()) for line in ''.join(self.parts).splitlines() if line.strip())

def capture(source, replace=False):
    target = ROOT / source['snapshot_path']
    target.parent.mkdir(parents=True, exist_ok=True)
    extracted = target.with_suffix('.txt')
    if target.exists() and not replace:
        raw = target.read_bytes()
        old_log=ROOT/'data/private/B01/capture_log.csv'
        previous={}
        if old_log.exists():
            with old_log.open(newline='',encoding='utf-8') as inp:
                previous=next((r for r in csv.DictReader(inp) if r['source_id']==source['source_id']),{})
        return dict(source_id=source['source_id'], status='existing_snapshot', sha256=hashlib.sha256(raw).hexdigest(), size_bytes=len(raw), captured_at_utc=previous.get('captured_at_utc',''), final_url=previous.get('final_url',''), content_type=previous.get('content_type',''), elapsed_seconds='', error='')
    started = time.monotonic()
    try:
        request = urllib.request.Request(source['url'], headers={'User-Agent': 'Mozilla/5.0 (research source capture)'})
        with urllib.request.urlopen(request, timeout=30) as response:
            raw = response.read()
            final_url = response.geturl()
            content_type = response.headers.get('Content-Type', '')
            charset = response.headers.get_content_charset() or 'utf-8'
        if 'html' not in content_type or b'<html' not in raw[:500].lower():
            raise ValueError('Expected HTML; response requires manual review')
        target.write_bytes(raw)
        parser = TextExtractor()
        parser.feed(raw.decode(charset, errors='replace'))
        extracted.write_text(parser.text(), encoding='utf-8')
        return dict(source_id=source['source_id'], status='downloaded', sha256=hashlib.sha256(raw).hexdigest(), size_bytes=len(raw), captured_at_utc=datetime.now(timezone.utc).isoformat(), final_url=final_url, content_type=content_type, elapsed_seconds=round(time.monotonic()-started, 2), error='')
    except Exception as exc:
        return dict(source_id=source['source_id'], status='retrieval_failed', sha256='', size_bytes='', captured_at_utc=datetime.now(timezone.utc).isoformat(), final_url='', content_type='', elapsed_seconds=round(time.monotonic()-started, 2), error=str(exc))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--replace', action='store_true', help='Explicitly replace local snapshots; otherwise preserve existing bytes')
    args = parser.parse_args()
    sources = json.loads((ROOT/'data/batches/B01/sources.json').read_text())
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
        results = list(pool.map(lambda source: capture(source, args.replace), sources))
    path = ROOT/'data/private/B01/capture_log.csv'
    with path.open('w', newline='', encoding='utf-8') as output:
        writer = csv.DictWriter(output, fieldnames=list(results[0]))
        writer.writeheader()
        writer.writerows(results)
    print(json.dumps({'downloaded':sum(r['status']=='downloaded' for r in results),'existing':sum(r['status']=='existing_snapshot' for r in results),'failed':sum(r['status']=='retrieval_failed' for r in results)}))

if __name__ == '__main__':
    main()
