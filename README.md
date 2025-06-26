# DevBrief
## 🛠️ Tech Stack

- **AWS Lambda** (Python 3.10) — Serverless compute for each stage
- **Amazon EventBridge (CloudWatch Events)** — Daily trigger
- **AWS Secrets Manager** — Secure API key storage
- **Amazon SES / Slack Webhook** — Delivery mechanisms
- **OpenAI / Gemini API** — Article summarization
- **GitHub Actions (Optional)** — CI/CD deployment

## 🧱 Architecture Overview

1. **Fetch & Parse**  
   Daily, a Lambda function scrapes RSS feeds and extracts titles, links, and snippets.

2. **Summarize**  
   The extracted items are passed to another Lambda, which uses OpenAI or Gemini API to generate concise summaries.

3. **Deliver**  
   A third Lambda sends the TL;DR as an email via Amazon SES or as a Slack message.

4. **Orchestration**  
   Scheduled with EventBridge. Can optionally use AWS Step Functions for chaining and error handling.

