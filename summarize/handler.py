import os
import json
import openai

# Get API key securely
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

MODEL = "gpt-4.1-mini"

def summarize_article(title, link, snippet):
    prompt = (
        f"Summarize this tech article in 2–3 concise bullets.\n\n"
        f"Title: {title}\n"
        f"Snippet: {snippet}\n\n"
        f"Format: - Bullet 1\n- Bullet 2\n- Bullet 3 (if needed)"
    )

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5
        )
        return {
            "title": title,
            "link": link,
            "summary": response.choices[0].message.content.strip()
        }
    except Exception as e:
        return {
            "title": title,
            "link": link,
            "summary": f"❌ Error: {str(e)}"
        }

def lambda_handler(event, context):
    if isinstance(event.get("body"), str):
        articles = json.loads(event["body"])
    else:
        articles = event.get("body", [])

    summarized = [summarize_article(a["title"], a["link"], a["summary"]) for a in articles]

    return {
        "statusCode": 200,
        "body": json.dumps(summarized, indent=2)
    }
