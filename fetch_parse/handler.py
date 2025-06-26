import json
import feedparser

# 🔁 Hardcoded feed URLs
FEED_URLS = [
    "https://hnrss.org/frontpage",
    "https://medium.com/feed/tag/technology",
    "https://github.com/trending"
]

def parse_feed(feed_url, limit=5):
    parsed = feedparser.parse(feed_url)
    entries = parsed.entries[:limit]
    result = []
    for entry in entries:
        result.append({
            "title": entry.get("title", "No title"),
            "link": entry.get("link", ""),
            "summary": entry.get("summary", "")[:300]
        })
    return result

def lambda_handler(event, context):
    all_items = []

    for url in FEED_URLS:
        try:
            items = parse_feed(url)
            all_items.extend(items)
        except Exception as e:
            print(f"Error parsing {url}: {str(e)}")

    return {
        "statusCode": 200,
        "body": json.dumps(all_items, indent=2)
    }
