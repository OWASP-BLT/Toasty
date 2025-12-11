"""
Utilities for GitHub App authentication and API interactions.
"""

import hashlib
import hmac
import time
from pathlib import Path

import jwt
import requests
from django.conf import settings


class GitHubAppAuth:
    """Handle GitHub App authentication and API requests."""

    def __init__(self):
        self.app_id = settings.GITHUB_APP_ID
        self.private_key = self._load_private_key()
        self.installation_id = settings.GITHUB_APP_INSTALLATION_ID

    def _load_private_key(self):
        """Load the private key from file or environment variable."""
        # Try to load from environment variable first
        if settings.GITHUB_APP_PRIVATE_KEY:
            return settings.GITHUB_APP_PRIVATE_KEY.replace("\\n", "\n")

        # Otherwise load from file
        if settings.GITHUB_APP_PRIVATE_KEY_PATH:
            key_path = Path(settings.GITHUB_APP_PRIVATE_KEY_PATH)
            if key_path.exists():
                return key_path.read_text()

        raise ValueError("GitHub App private key not found in environment variables or file path")

    def generate_jwt(self):
        """Generate a JWT for authenticating as a GitHub App."""
        now = int(time.time())
        payload = {
            "iat": now - 60,  # Issued at time (60 seconds in the past to allow for clock drift)
            "exp": now + (10 * 60),  # Expiration time (10 minutes from now)
            "iss": self.app_id,
        }

        return jwt.encode(payload, self.private_key, algorithm="RS256")

    def get_installation_access_token(self):
        """Get an installation access token for making API requests."""
        jwt_token = self.generate_jwt()

        headers = {
            "Authorization": f"Bearer {jwt_token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }

        url = f"https://api.github.com/app/installations/{self.installation_id}/access_tokens"
        response = requests.post(url, headers=headers, timeout=10)
        response.raise_for_status()

        return response.json()["token"]

    def create_comment(self, owner, repo, issue_number, body):
        """Create a comment on an issue or pull request."""
        token = self.get_installation_access_token()

        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }

        url = f"https://api.github.com/repos/{owner}/{repo}/issues/{issue_number}/comments"
        data = {"body": body}

        response = requests.post(url, headers=headers, json=data, timeout=10)
        response.raise_for_status()

        return response.json()


def verify_webhook_signature(request):
    """
    Verify that the webhook request came from GitHub.

    Args:
        request: Django HttpRequest object

    Returns:
        bool: True if signature is valid, False otherwise
    """
    signature_header = request.headers.get("X-Hub-Signature-256")
    if not signature_header:
        return False

    webhook_secret = settings.GITHUB_WEBHOOK_SECRET
    if not webhook_secret:
        return False

    # Calculate expected signature
    expected_signature = "sha256=" + hmac.new(
        webhook_secret.encode("utf-8"), request.body, hashlib.sha256
    ).hexdigest()

    # Use constant-time comparison to prevent timing attacks
    return hmac.compare_digest(signature_header, expected_signature)
