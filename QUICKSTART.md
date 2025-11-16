# Quick Start Guide

Get Toasty up and running in 5 minutes!

## Prerequisites

- Python 3.11+
- GitHub account
- Google Gemini API key ([Get one here](https://ai.google.dev/))
- GitHub Personal Access Token ([Create one here](https://github.com/settings/tokens))

## Setup

### 1. Clone and Install

```bash
git clone https://github.com/OWASP-BLT/Toasty.git
cd Toasty
pip install -r requirements.txt
```

### 2. Configure Environment

Create a `.env` file:

```bash
cp .env.example .env
```

Edit `.env` with your credentials:

```env
GITHUB_TOKEN=ghp_your_github_token_here
GITHUB_WEBHOOK_SECRET=your_random_secret_here
GEMINI_API_KEY=your_gemini_api_key_here
```

**Generate a secure webhook secret:**
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### 3. Run the Bot

```bash
python -m toasty.main
```

The bot will start on `http://localhost:8000`

### 4. Test Locally

```bash
# Check health
curl http://localhost:8000/health

# Expected response:
# {"status":"healthy","app":"Toasty","version":"0.1.0"}
```

## GitHub Webhook Setup

### Option 1: Local Testing with ngrok

1. **Install ngrok**
   ```bash
   brew install ngrok  # macOS
   # or download from https://ngrok.com/download
   ```

2. **Expose local server**
   ```bash
   ngrok http 8000
   ```

3. **Copy the HTTPS URL** (e.g., `https://abc123.ngrok.io`)

4. **Configure GitHub webhook:**
   - Go to your repository → Settings → Webhooks → Add webhook
   - Payload URL: `https://abc123.ngrok.io/webhook`
   - Content type: `application/json`
   - Secret: (same as `GITHUB_WEBHOOK_SECRET` in `.env`)
   - Events: Pull requests, Issues, Issue comments
   - Active: ✓

### Option 2: Deploy to Cloud

See [README.md](README.md) for deployment options (Docker, Heroku, Cloud Run).

## Quick Test

1. **Create a test pull request** in your repository

2. **Wait for Toasty** to analyze it (usually 10-30 seconds)

3. **Check the PR** for an automated review comment like:
   ```
   🤖 Automated Code Review by Toasty
   
   Overall Assessment: APPROVE
   
   Security: ✓ No security concerns found
   Code Quality: ✓ Looks good
   ...
   ```

## Usage Examples

### Get a Code Review

Open a pull request, and Toasty will automatically:
- Fetch the diff
- Analyze with AI
- Post a comprehensive review

### Get Issue Help

Create an issue, and Toasty will:
- Categorize the issue
- Suggest labels
- Provide initial guidance

### Ask Questions

Mention the bot in any comment:
```
@toasty-bot can you explain this approach?
```

Toasty will respond with contextual help!

## Troubleshooting

### Bot not responding?

1. **Check logs:**
   ```bash
   # Look for errors in the console where you ran the bot
   ```

2. **Verify webhook:**
   - Go to Settings → Webhooks
   - Click your webhook
   - Check "Recent Deliveries"
   - Look for failed deliveries

3. **Test signature:**
   ```bash
   # Ensure GITHUB_WEBHOOK_SECRET matches in:
   # - .env file
   # - GitHub webhook settings
   ```

### AI not generating responses?

1. **Check Gemini API key:**
   ```bash
   # Verify it's set correctly in .env
   echo $GEMINI_API_KEY
   ```

2. **Check API quota:**
   - Visit [Google AI Studio](https://ai.google.dev/)
   - Check your usage limits

### Permission errors?

Ensure your GitHub token has:
- `repo` scope (full repository access)
- `write:discussion` scope (for comments)

## Next Steps

- Customize AI prompts in `toasty/services/ai.py`
- Add custom event handlers in `toasty/handlers/`
- Deploy to production (see README.md)
- Contribute improvements!

## Need Help?

- 📖 Read the [full documentation](README.md)
- 🐛 Report issues on [GitHub](https://github.com/OWASP-BLT/Toasty/issues)
- 💬 Join the discussion

Happy reviewing! 🎉
