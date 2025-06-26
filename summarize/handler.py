import json
import os
import openai  # or google.generativeai for Gemini

# Set your OpenAI API key via Lambda env variable or Secrets Manager
openai.api_key = os.getenv("OPENAI_API_KEY")

# 📌 Summarize one article using OpenAI
def summarize_article(title, link, snippet):
    prompt = (
        f"Summarize this tech article in 2–3 concise bullets.\n\n"
        f"Title: {title}\n"
        f"Snippet: {snippet}\n\n"
        f"Format: - Bullet 1\n- Bullet 2\n- Bullet 3 (if needed)"
    )
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",  # or gpt-3.5-turbo
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
        )
        summary = response['choices'][0]['message']['content']
        return {
            "title": title,
            "link": link,
            "summary": summary
        }
    except Exception as e:
        return {
            "title": title,
            "link": link,
            "summary": f"❌ Error generating summary: {str(e)}"
        }

def lambda_handler(event, context):
    # event['body'] is a JSON string if called from API Gateway
    if isinstance(event.get("body"), str):
        articles = json.loads(event["body"])
    else:
        articles = event.get("body", [])

    summarized = [summarize_article(a["title"], a["link"], a["summary"]) for a in articles]

    return {
        "statusCode": 200,
        "body": json.dumps(summarized, indent=2)
    }

