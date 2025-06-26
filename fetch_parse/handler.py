import json
import feedparser
import os

def load_feeds(file_path='feeds.json'):
    with open(file_path, 'r') as f:
        return json.load(f)

def parse_feed(feed_url, limit=5):
    parsed = feedparser.parse(feed_url)
    entries = parsed.entries[:limit]
    result = []
    for entry in entries:
        result.append({
            "title": entry.get("title", "No title"),
            "link": entry.get("link", ""),
            "summary": entry.get("summary", "")[:300]  # Truncate long summaries
        })
    return result

def lambda_handler(event, context):
    feeds = load_feeds()
    all_items = []

    for url in feeds:
        try:
            items = parse_feed(url)
            all_items.extend(items)
        except Exception as e:
            print(f"Error parsing {url}: {str(e)}")

    # Return combined feed items for summarization
    return {
        "statusCode": 200,
        "body": json.dumps(all_items, indent=2)
    }

