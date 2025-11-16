"""GitHub utility functions."""

import hmac
import hashlib
import logging
from typing import Optional

import requests

from toasty.config import settings

logger = logging.getLogger(__name__)


def verify_signature(payload_body: bytes, signature_header: str) -> bool:
    """
    Verify the GitHub webhook signature using HMAC SHA256.

    Args:
        payload_body: Raw request body as bytes
        signature_header: Value from 'X-Hub-Signature-256' header

    Returns:
        True if signature is valid, False otherwise
    """
    if not signature_header or not signature_header.startswith("sha256="):
        logger.warning("Invalid signature header format")
        return False

    if not settings.github_webhook_secret:
        logger.error("Webhook secret not configured")
        return False

    try:
        received_signature = signature_header.split("=", 1)[1]
    except IndexError:
        logger.warning("Failed to extract signature from header")
        return False

    mac = hmac.new(settings.github_webhook_secret.encode(), payload_body, hashlib.sha256)
    expected_signature = mac.hexdigest()

    return hmac.compare_digest(expected_signature, received_signature)


def get_pr_diff(owner: str, repo: str, pr_number: int) -> Optional[str]:
    """
    Fetch pull request diff from GitHub API.

    Args:
        owner: Repository owner
        repo: Repository name
        pr_number: Pull request number

    Returns:
        Diff text or None if failed
    """
    url = f"{settings.github_api_url}/repos/{owner}/{repo}/pulls/{pr_number}"
    headers = {
        "Authorization": f"Bearer {settings.github_token}",
        "Accept": "application/vnd.github.v3.diff",
        "User-Agent": f"{settings.github_bot_username}/1.0",
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        logger.error(f"Failed to fetch PR diff: {e}")
        return None


def get_pr_files(owner: str, repo: str, pr_number: int) -> Optional[list]:
    """
    Fetch list of files changed in a pull request.

    Args:
        owner: Repository owner
        repo: Repository name
        pr_number: Pull request number

    Returns:
        List of file information or None if failed
    """
    url = f"{settings.github_api_url}/repos/{owner}/{repo}/pulls/{pr_number}/files"
    headers = {
        "Authorization": f"Bearer {settings.github_token}",
        "Accept": "application/vnd.github+json",
        "User-Agent": f"{settings.github_bot_username}/1.0",
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logger.error(f"Failed to fetch PR files: {e}")
        return None


def post_comment(owner: str, repo: str, issue_number: int, body: str) -> Optional[dict]:
    """
    Post a comment on a GitHub issue or pull request.

    Args:
        owner: Repository owner
        repo: Repository name
        issue_number: Issue or PR number
        body: Comment body

    Returns:
        Comment data or None if failed
    """
    url = f"{settings.github_api_url}/repos/{owner}/{repo}/issues/{issue_number}/comments"
    headers = {
        "Authorization": f"Bearer {settings.github_token}",
        "Accept": "application/vnd.github+json",
        "Content-Type": "application/json",
        "User-Agent": f"{settings.github_bot_username}/1.0",
    }

    try:
        response = requests.post(url, json={"body": body}, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logger.error(f"Failed to post comment: {e}")
        return None


def update_comment(owner: str, repo: str, comment_id: int, body: str) -> Optional[dict]:
    """
    Update an existing GitHub comment.

    Args:
        owner: Repository owner
        repo: Repository name
        comment_id: Comment ID
        body: Updated comment body

    Returns:
        Comment data or None if failed
    """
    url = f"{settings.github_api_url}/repos/{owner}/{repo}/issues/comments/{comment_id}"
    headers = {
        "Authorization": f"Bearer {settings.github_token}",
        "Accept": "application/vnd.github+json",
        "Content-Type": "application/json",
        "User-Agent": f"{settings.github_bot_username}/1.0",
    }

    try:
        response = requests.patch(url, json={"body": body}, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logger.error(f"Failed to update comment: {e}")
        return None


def get_issue_comments(owner: str, repo: str, issue_number: int) -> Optional[list]:
    """
    Get all comments on an issue or pull request.

    Args:
        owner: Repository owner
        repo: Repository name
        issue_number: Issue or PR number

    Returns:
        List of comments or None if failed
    """
    url = f"{settings.github_api_url}/repos/{owner}/{repo}/issues/{issue_number}/comments"
    headers = {
        "Authorization": f"Bearer {settings.github_token}",
        "Accept": "application/vnd.github+json",
        "User-Agent": f"{settings.github_bot_username}/1.0",
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logger.error(f"Failed to fetch comments: {e}")
        return None


def find_bot_comment(owner: str, repo: str, issue_number: int, marker: str) -> Optional[dict]:
    """
    Find an existing comment made by the bot with a specific marker.

    Args:
        owner: Repository owner
        repo: Repository name
        issue_number: Issue or PR number
        marker: Unique marker to identify bot comments

    Returns:
        Comment data or None if not found
    """
    comments = get_issue_comments(owner, repo, issue_number)
    if not comments:
        return None

    bot_username = settings.github_bot_username.lower()
    marker_lower = marker.lower()

    for comment in comments:
        author = comment.get("user", {}).get("login", "").lower()
        body = comment.get("body", "").lower()
        if author == bot_username and marker_lower in body:
            return comment

    return None
