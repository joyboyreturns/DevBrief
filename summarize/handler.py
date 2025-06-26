import os
import json
import google.generativeai as genai

# Get API key from environment variable
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("models/gemini-1.5-flash")

def summarize_article(title, link, snippet):
    prompt = (
        f"Summarize this tech article in 2–3 concise bullets.\n\n"
        f"Title: {title}\n"
        f"Snippet: {snippet}\n\n"
        f"Format: - Bullet 1\n- Bullet 2\n- Bullet 3 (if needed)"
    )

    try:
        response = model.generate_content(prompt)
        return {
            "title": title,
            "link": link,
            "summary": response.text
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
