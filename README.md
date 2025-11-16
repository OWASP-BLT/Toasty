# Toasty 🤖

AI-powered GitHub bot for automated code reviews, project management, and security analysis.

## Features

### 🔍 AI Code Reviews
- **Automated PR Analysis**: Comprehensive code reviews using Google's Gemini AI
- **Security-Focused**: Identifies potential vulnerabilities and security risks
- **Best Practices**: Checks for code quality, performance, and maintainability
- **Contextual Comments**: Posts detailed reviews directly on pull requests

### 🛡️ Security Analysis
- **Vulnerability Detection**: Scans code for common security issues
- **Secure Coding Practices**: Ensures adherence to security best practices
- **Dependency Scanning**: (Future) Identifies vulnerable dependencies

### 📋 Project Management
- **Issue Triage**: Automatically categorizes and prioritizes issues
- **Smart Labeling**: Suggests appropriate labels based on issue content
- **Helpful Responses**: Provides initial guidance and asks clarifying questions

### 💬 Interactive Bot
- **Mention Support**: Responds to @mentions in comments
- **Contextual Help**: Provides assistance based on PR/issue context
- **Friendly Interface**: Professional and helpful communication style

## Architecture

```
toasty/
├── api/                 # FastAPI application and endpoints
│   └── app.py          # Main webhook handler
├── handlers/           # Event handlers for GitHub webhooks
│   ├── pr_handler.py   # Pull request events
│   ├── issue_handler.py # Issue events
│   └── comment_handler.py # Comment events
├── services/           # External service integrations
│   └── ai.py          # Gemini AI integration
├── utils/             # Utility functions
│   ├── github.py      # GitHub API interactions
│   └── validation.py  # Payload validation
├── schemas/           # JSON schemas for webhook validation
│   ├── pr_schema.json
│   ├── issue_schema.json
│   └── comment_schema.json
├── config.py          # Configuration management
└── main.py           # Application entry point
```

## Installation

### Prerequisites
- Python 3.11 or higher
- GitHub account with repository access
- Google Gemini API key
- GitHub Personal Access Token

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/OWASP-BLT/Toasty.git
   cd Toasty
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   
   Or with Poetry:
   ```bash
   poetry install
   ```

3. **Configure environment variables**
   
   Create a `.env` file in the root directory:
   ```env
   # GitHub Configuration
   GITHUB_TOKEN=your_github_token
   GITHUB_WEBHOOK_SECRET=your_webhook_secret
   GITHUB_BOT_USERNAME=toasty-bot
   
   # AI Configuration
   GEMINI_API_KEY=your_gemini_api_key
   GEMINI_MODEL=gemini-2.0-flash
   
   # Application Configuration
   DEBUG=false
   HOST=0.0.0.0
   PORT=8000
   ```

4. **Run the bot**
   ```bash
   python -m toasty.main
   ```
   
   Or with uvicorn directly:
   ```bash
   uvicorn toasty.api.app:app --host 0.0.0.0 --port 8000
   ```

## GitHub Webhook Configuration

1. **Navigate to your repository settings**
   - Go to Settings → Webhooks → Add webhook

2. **Configure the webhook**
   - **Payload URL**: `https://your-domain.com/webhook`
   - **Content type**: `application/json`
   - **Secret**: Same as `GITHUB_WEBHOOK_SECRET` in your `.env` file
   - **Events**: Select individual events:
     - Pull requests
     - Issues
     - Issue comments

3. **Save the webhook**
   - GitHub will send a ping event to verify the connection

## API Endpoints

### `GET /health`
Health check endpoint to verify the bot is running.

**Response:**
```json
{
  "status": "healthy",
  "app": "Toasty",
  "version": "0.1.0"
}
```

### `POST /webhook`
Main webhook endpoint for receiving GitHub events.

**Headers:**
- `X-GitHub-Event`: Type of GitHub event
- `X-Hub-Signature-256`: HMAC signature for verification

**Supported Events:**
- `pull_request`: opened, synchronize, reopened
- `issues`: opened, edited, reopened
- `issue_comment`: created, edited

## Usage Examples

### Automated PR Review

When a pull request is opened:
1. Toasty fetches the PR diff and files
2. Analyzes the changes using Gemini AI
3. Posts a comprehensive review comment with:
   - Overall assessment
   - Security concerns
   - Code quality issues
   - Performance suggestions
   - Best practice recommendations

### Issue Analysis

When an issue is created:
1. Toasty analyzes the issue title and description
2. Categorizes the issue type
3. Suggests appropriate labels
4. Provides initial guidance
5. Asks clarifying questions if needed

### Interactive Mentions

Mention the bot in any comment:
```
@toasty-bot can you review this section?
```

The bot will:
1. Detect the mention
2. Understand the context
3. Provide a helpful response

## Development

### Running Tests

```bash
pytest
```

With coverage:
```bash
pytest --cov=toasty --cov-report=html
```

### Code Quality

Format code with Black:
```bash
black toasty/
```

Lint with Ruff:
```bash
ruff check toasty/
```

Type checking with mypy:
```bash
mypy toasty/
```

## Security Considerations

- **Webhook Signature Verification**: All webhooks are verified using HMAC-SHA256
- **Environment Variables**: Secrets are stored in environment variables, never in code
- **Input Validation**: All payloads are validated against JSON schemas
- **Rate Limiting**: Implements retry logic with exponential backoff
- **Least Privilege**: GitHub token should have minimal required permissions

## Configuration

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `GITHUB_TOKEN` | GitHub personal access token | Yes | - |
| `GITHUB_WEBHOOK_SECRET` | Webhook secret for signature verification | Yes | - |
| `GITHUB_BOT_USERNAME` | GitHub username of the bot | No | `toasty-bot` |
| `GEMINI_API_KEY` | Google Gemini API key | Yes | - |
| `GEMINI_MODEL` | Gemini model to use | No | `gemini-2.0-flash` |
| `DEBUG` | Enable debug mode | No | `false` |
| `HOST` | Server host | No | `0.0.0.0` |
| `PORT` | Server port | No | `8000` |

### GitHub Token Permissions

The GitHub token needs the following permissions:
- `repo`: Full repository access
- `write:discussion`: Create and edit comments

## Deployment

### Docker (Coming Soon)

```bash
docker build -t toasty .
docker run -p 8000:8000 --env-file .env toasty
```

### Heroku

```bash
heroku create toasty-bot
heroku config:set GITHUB_TOKEN=your_token
heroku config:set GEMINI_API_KEY=your_key
git push heroku main
```

### Cloud Run

```bash
gcloud run deploy toasty \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

## Roadmap

- [ ] Dependency vulnerability scanning
- [ ] Advanced security analysis with custom rules
- [ ] Integration with issue trackers (Jira, Linear)
- [ ] Automated milestone management
- [ ] Custom AI prompts via configuration
- [ ] Multi-repository support
- [ ] Dashboard for analytics
- [ ] Slack/Discord notifications

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

This project is licensed under the AGPL-3.0 License - see the LICENSE file for details.

## Credits

Built with ❤️ by the OWASP BLT Team

Powered by:
- [FastAPI](https://fastapi.tiangolo.com/)
- [Google Gemini](https://ai.google.dev/)
- [GitHub API](https://docs.github.com/en/rest)

## Support

For issues, questions, or contributions:
- GitHub Issues: [OWASP-BLT/Toasty/issues](https://github.com/OWASP-BLT/Toasty/issues)
- Documentation: [Wiki](https://github.com/OWASP-BLT/Toasty/wiki)

---

**Note**: This bot uses AI to analyze code and may not catch all issues. Always review AI-generated comments critically and use your judgment.
