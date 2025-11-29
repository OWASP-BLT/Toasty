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

response = client.chat.completions(
    messages=[
        {'role': 'system', 'content': 'You are a Pull Request (PR) analyzer. You classify them into the follwing categories: Bug Fix, Feature Addition, Documentation Update, Performance Improvement, Refactoring, Testing, and Others. Based on the content of the PR title and body, no need to provide a concise classification along with a brief explanation for your choice.'},
        {"role": "user", "content": lol}
    ],
    temperature=0.5,
    top_p=1,
    max_tokens=1000,
)

print(response.choices[0].message.content)
