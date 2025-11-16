"""Handler for pull request events."""

import logging
from typing import Any, Dict

from toasty.config import settings
from toasty.services.ai import ai_service
from toasty.utils.github import find_bot_comment, get_pr_diff, get_pr_files, post_comment, update_comment
from toasty.utils.validation import validate_pr_payload

logger = logging.getLogger(__name__)

PR_REVIEW_MARKER = "🤖 **Automated Code Review by Toasty**"


def handle_pr_opened(payload: Dict[str, Any]) -> None:
    """
    Handle newly opened pull requests.

    Args:
        payload: GitHub webhook payload
    """
    try:
        validate_pr_payload(payload)
    except Exception as e:
        logger.error(f"Invalid PR payload: {e}")
        return

    pr = payload.get("pull_request", {})
    repo = payload.get("repository", {})
    
    pr_number = pr.get("number")
    pr_title = pr.get("title", "No title")
    pr_body = pr.get("body", "No description")
    owner = repo.get("owner", {}).get("login")
    repo_name = repo.get("name")

    logger.info(f"Handling new PR #{pr_number} in {owner}/{repo_name}")

    # Fetch PR diff and files
    diff = get_pr_diff(owner, repo_name, pr_number)
    files = get_pr_files(owner, repo_name, pr_number)

    if not diff:
        logger.warning(f"Could not fetch diff for PR #{pr_number}")
        return

    # Generate AI review
    review = ai_service.analyze_pr(pr_title, pr_body, diff, files or [])
    
    if not review:
        logger.error(f"Failed to generate review for PR #{pr_number}")
        return

    # Post review as comment
    comment_body = f"{PR_REVIEW_MARKER}\n\n{review}"
    result = post_comment(owner, repo_name, pr_number, comment_body)

    if result:
        logger.info(f"Successfully posted review for PR #{pr_number}")
    else:
        logger.error(f"Failed to post review for PR #{pr_number}")


def handle_pr_synchronize(payload: Dict[str, Any]) -> None:
    """
    Handle pull request updates (new commits pushed).

    Args:
        payload: GitHub webhook payload
    """
    try:
        validate_pr_payload(payload)
    except Exception as e:
        logger.error(f"Invalid PR payload: {e}")
        return

    pr = payload.get("pull_request", {})
    repo = payload.get("repository", {})
    
    pr_number = pr.get("number")
    pr_title = pr.get("title", "No title")
    pr_body = pr.get("body", "No description")
    owner = repo.get("owner", {}).get("login")
    repo_name = repo.get("name")

    logger.info(f"Handling PR update #{pr_number} in {owner}/{repo_name}")

    # Fetch updated diff and files
    diff = get_pr_diff(owner, repo_name, pr_number)
    files = get_pr_files(owner, repo_name, pr_number)

    if not diff:
        logger.warning(f"Could not fetch diff for PR #{pr_number}")
        return

    # Generate updated review
    review = ai_service.analyze_pr(pr_title, pr_body, diff, files or [])
    
    if not review:
        logger.error(f"Failed to generate review for PR #{pr_number}")
        return

    # Check if we already have a comment
    existing_comment = find_bot_comment(owner, repo_name, pr_number, PR_REVIEW_MARKER)

    comment_body = f"{PR_REVIEW_MARKER}\n\n{review}\n\n---\n*Updated: New commits pushed*"

    if existing_comment:
        # Update existing comment
        comment_id = existing_comment.get("id")
        result = update_comment(owner, repo_name, comment_id, comment_body)
        if result:
            logger.info(f"Successfully updated review for PR #{pr_number}")
        else:
            logger.error(f"Failed to update review for PR #{pr_number}")
    else:
        # Post new comment
        result = post_comment(owner, repo_name, pr_number, comment_body)
        if result:
            logger.info(f"Successfully posted review for PR #{pr_number}")
        else:
            logger.error(f"Failed to post review for PR #{pr_number}")


def handle_pr_event(payload: Dict[str, Any]) -> None:
    """
    Main handler for pull request events.

    Args:
        payload: GitHub webhook payload
    """
    action = payload.get("action")
    
    if action == "opened":
        handle_pr_opened(payload)
    elif action == "synchronize":
        handle_pr_synchronize(payload)
    elif action == "reopened":
        handle_pr_opened(payload)
    else:
        logger.info(f"Ignoring PR action: {action}")
