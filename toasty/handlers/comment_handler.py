"""Handler for comment events."""

import logging
from typing import Any, Dict

from toasty.config import settings
from toasty.services.ai import ai_service
from toasty.utils.github import post_comment
from toasty.utils.validation import validate_comment_payload

logger = logging.getLogger(__name__)


def handle_comment_created(payload: Dict[str, Any]) -> None:
    """
    Handle newly created comments.

    Args:
        payload: GitHub webhook payload
    """
    try:
        validate_comment_payload(payload)
    except Exception as e:
        logger.error(f"Invalid comment payload: {e}")
        return

    comment = payload.get("comment", {})
    issue = payload.get("issue", {})
    repo = payload.get("repository", {})
    
    comment_body = comment.get("body", "")
    commenter = comment.get("user", {}).get("login")
    issue_number = issue.get("number")
    owner = repo.get("owner", {}).get("login")
    repo_name = repo.get("name")

    # Ignore comments by the bot itself
    if commenter.lower() == settings.github_bot_username.lower():
        logger.info("Ignoring comment by bot itself")
        return

    # Check if bot is mentioned
    bot_mention = f"@{settings.github_bot_username}"
    if bot_mention.lower() not in comment_body.lower():
        logger.info("Bot not mentioned in comment, ignoring")
        return

    logger.info(f"Bot mentioned in comment on #{issue_number} in {owner}/{repo_name}")

    # Determine if this is a PR or issue
    is_pr = "pull_request" in issue
    context_type = "Pull Request" if is_pr else "Issue"

    # Build context for AI
    issue_title = issue.get("title", "No title")
    context = f"{context_type} #{issue_number}: {issue_title}"

    # Generate AI response
    response = ai_service.respond_to_comment(comment_body, context)
    
    if not response:
        logger.error(f"Failed to generate response for comment on #{issue_number}")
        return

    # Post response
    response_body = f"Hi @{commenter}! 👋\n\n{response}"
    result = post_comment(owner, repo_name, issue_number, response_body)

    if result:
        logger.info(f"Successfully responded to comment on #{issue_number}")
    else:
        logger.error(f"Failed to respond to comment on #{issue_number}")


def handle_comment_event(payload: Dict[str, Any]) -> None:
    """
    Main handler for comment events.

    Args:
        payload: GitHub webhook payload
    """
    action = payload.get("action")
    
    if action == "created":
        handle_comment_created(payload)
    else:
        logger.info(f"Ignoring comment action: {action}")
