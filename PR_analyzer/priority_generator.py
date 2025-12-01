from sarvamai import SarvamAI
#from dotenv import load_dotenv
import os

#load_dotenv()   # only if using .env
client = SarvamAI(api_subscription_key=os.getenv("SARVAM_API_KEY"))
#client = SarvamAI(api_subscription_key=os.getenv("SARVAM_API_KEY"))

lol = """Title: project, dev and docker setup
Body: Initial setup for further development
- Django installation
- Docker and docker-compose configuration
- Linting, security, formatting, and testing tools setup"""


lol2 = """
Title: Migrate BLT-AIBot from OWASP-BLT/BLT to Toasty repository
Body: Migrates the complete BLT-AIBot codebase from [PR #4522](https://github.com/OWASP-BLT/BLT/pull/4522) to this dedicated Toasty repository.

Fixes #1 #2 #3 #4 #5 #6 #11

## AIBot Django App (`toasty/aibot/`)

- **Webhook Handler** (`main.py`): GitHub webhook endpoint processing PR, issue, installation, push, and comment events
- **Celery Tasks** (`tasks.py`): Background processing for AI-powered PR reviews, issue analysis, and comment responses
- **Gemini Integration** (`gemini_api.py`): Text generation and embedding via Google Gemini
- **Qdrant Integration** (`qdrant_api.py`): Semantic code search, collection management, embedding storage
- **GitHub API** (`github_api.py`, `gh_token_manager.py`): JWT-based auth, installation token caching, API client with retry logic
- **Code Chunking** (`chunk_utils.py`): AST-aware Python chunking, YAML/JSON/HTML handlers, token-aware splitting
- **Models** (`db_models.py`): `GithubAppInstallation`, `GithubAppRepo`, `AibotComment`

## Infrastructure

- **Docker Compose**: PostgreSQL, Redis, Qdrant, Celery worker services
- **Settings**: Environment-based config for all services, production SECRET_KEY enforcement
- **Dependencies**: google-genai, qdrant-client, celery[redis], langchain, psycopg2-binary

## Endpoints

```python
path("aibot/", aibot_webhook_entrypoint, name="aibot_webhook_entrypoint")
path("aibot/health/", aibot_health_check, name="aibot_health_check")
```

## Configuration

See `.env.example` for required environment variables including GitHub App credentials, Gemini API key, and Qdrant settings.

<!-- START COPILOT CODING AGENT SUFFIX -->



<details>

<summary>Original prompt</summary>

> move this PR to here https://github.com/OWASP-BLT/BLT/pull/4522


</details>
"""




response = client.chat.completions(
    messages=[
        {'role': 'system', 'content': 'You are a Pull Request (PR) analyzer. You classify them into the follwing categories: "Bug Fix", "Feature Addition", "Documentation Update", "Performance Improvement", "Refactoring", "Testing", and "Others". Based on the content of the PR title and body. No need to provide a concise classification along with a brief explanation for your choice.'},
        {"role": "user", "content": lol2}
    ],
    temperature=0.5,
    top_p=1,
    max_tokens=1000,
)

print(response.choices[0].message.content)
