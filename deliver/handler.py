import json
import os
import urllib.request

SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")

def format_slack_message(summaries):
    blocks = []
    for article in summaries:
        blocks.append({
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"*<{article['link']}|{article['title']}>*\n{article['summary']}"
            }
        })
        blocks.append({"type": "divider"})
    return { "blocks": blocks }

def lambda_handler(event, context):
    if isinstance(event.get("body"), str):
        summaries = json.loads(event["body"])
    else:
        summaries = event.get("body", [])

    payload = format_slack_message(summaries)
    data = json.dumps(payload).encode("utf-8")

    try:
        req = urllib.request.Request(
            SLACK_WEBHOOK_URL,
            data=data,
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req) as resp:
            return {
                "statusCode": resp.status,
                "body": f"Sent {len(summaries)} items to Slack"
            }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": f"❌ Slack delivery failed: {str(e)}"
        }
