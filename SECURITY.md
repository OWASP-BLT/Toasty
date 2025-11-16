# Security Policy

## Supported Versions

We release patches for security vulnerabilities. Currently supported versions:

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |

## Reporting a Vulnerability

We take the security of Toasty seriously. If you believe you have found a security vulnerability, please report it to us as described below.

### Please do NOT:

- Open a public GitHub issue
- Discuss the vulnerability in public forums
- Exploit the vulnerability

### Please DO:

1. **Report privately**: Send details to the maintainers via GitHub Security Advisories:
   - Go to the [Security tab](https://github.com/OWASP-BLT/Toasty/security)
   - Click "Report a vulnerability"
   - Fill out the form with details

2. **Include in your report:**
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)
   - Your contact information

3. **Wait for acknowledgment**: We will acknowledge your email within 48 hours.

### What to expect:

- **Initial Response**: Within 48 hours
- **Status Update**: Within 7 days
- **Fix Timeline**: Depends on severity
  - Critical: Within 7 days
  - High: Within 14 days
  - Medium: Within 30 days
  - Low: Within 90 days

### Disclosure Policy

- We request that you give us reasonable time to fix the issue before public disclosure
- We will coordinate with you on the disclosure timeline
- We will credit you in the security advisory (unless you prefer to remain anonymous)

## Security Features

### Current Protections

- **Webhook Verification**: HMAC-SHA256 signature verification
- **Input Validation**: JSON schema validation for all webhooks
- **Secrets Management**: Environment variables, never in code
- **Dependency Scanning**: Automated vulnerability checks
- **Rate Limiting**: Exponential backoff for API calls
- **Least Privilege**: Minimal GitHub token permissions

### Best Practices for Deployment

1. **Use HTTPS**: Always use HTTPS for webhook endpoints
2. **Rotate Secrets**: Regularly rotate webhook secrets and API keys
3. **Monitor Logs**: Keep an eye on application logs for suspicious activity
4. **Update Dependencies**: Keep dependencies up to date
5. **Limit Permissions**: Use GitHub tokens with minimal required permissions
6. **Network Security**: Deploy behind a firewall or in a secure network
7. **Environment Isolation**: Use separate credentials for dev/staging/production

### Required GitHub Token Permissions

Toasty requires these permissions:
- `repo`: Full repository access (read PRs, post comments)
- `write:discussion`: Create and edit comments

**Never use tokens with more permissions than necessary.**

### Webhook Secret

Your webhook secret should be:
- At least 32 characters long
- Randomly generated (use `python -c "import secrets; print(secrets.token_hex(32))"`)
- Stored securely in environment variables
- Rotated periodically

### API Keys

- **Gemini API Key**: Keep private, monitor usage
- **GitHub Token**: Use fine-grained tokens when possible
- **Never commit**: Never commit secrets to version control

## Known Security Considerations

### AI-Generated Content

- AI-generated code reviews should not be blindly trusted
- Always review AI suggestions before applying them
- AI may miss certain types of vulnerabilities
- Human review is still essential

### Rate Limiting

- The bot implements rate limiting to prevent abuse
- Large repositories may take longer to analyze
- Consider setting up retry mechanisms

### Data Privacy

- The bot processes code from your repository
- Code is sent to Google Gemini API for analysis
- Ensure your organization's policies allow this
- Consider self-hosting AI models for sensitive code

## Security Checklist for Contributors

Before submitting code:

- [ ] No hardcoded secrets or credentials
- [ ] All user input is validated
- [ ] No SQL injection vulnerabilities
- [ ] No command injection vulnerabilities
- [ ] Proper error handling (no sensitive info in errors)
- [ ] Dependencies are up to date
- [ ] Tests cover security-critical code
- [ ] Documentation updated for security features

## Security Updates

Subscribe to security advisories:
- Watch the repository
- Enable notifications for security advisories
- Follow [@OWASP_BLT](https://twitter.com/owasp_blt) on Twitter

## Acknowledgments

We would like to thank the following individuals for responsibly disclosing security issues:

_None yet - be the first!_

## Questions?

For general security questions (not vulnerabilities), open a discussion in the repository.

---

**Remember**: Security is everyone's responsibility. If you see something, say something!
