"""Handler for issue events."""

import logging
from typing import Any, Dict

from toasty.services.ai import ai_service
from toasty.utils.github import find_bot_comment, post_comment, update_comment
from toasty.utils.validation import validate_issue_payload

logger = logging.getLogger(__name__)

ISSUE_ANALYSIS_MARKER = "🤖 **Issue Analysis by Toasty**"


def handle_issue_opened(payload: Dict[str, Any]) -> None:
    """
    Handle newly opened issues.

    Args:
        payload: GitHub webhook payload
    """
    try:
        validate_issue_payload(payload)
    except Exception as e:
        logger.error(f"Invalid issue payload: {e}")
        return

    issue = payload.get("issue", {})
    repo = payload.get("repository", {})

    issue_number = issue.get("number")
    issue_title = issue.get("title", "No title")
    issue_body = issue.get("body", "No description")
    owner = repo.get("owner", {}).get("login")
    repo_name = repo.get("name")

    logger.info(f"Handling new issue #{issue_number} in {owner}/{repo_name}")

    # Generate AI analysis
    analysis = ai_service.analyze_issue(issue_title, issue_body)

    if not analysis:
        logger.error(f"Failed to generate analysis for issue #{issue_number}")
        return

    # Post analysis as comment
    comment_body = f"{ISSUE_ANALYSIS_MARKER}\n\n{analysis}"
    result = post_comment(owner, repo_name, issue_number, comment_body)

    if result:
        logger.info(f"Successfully posted analysis for issue #{issue_number}")
    else:
        logger.error(f"Failed to post analysis for issue #{issue_number}")


def handle_issue_edited(payload: Dict[str, Any]) -> None:
    """
    Handle edited issues.

    Args:
        payload: GitHub webhook payload
    """
    try:
        validate_issue_payload(payload)
    except Exception as e:
        logger.error(f"Invalid issue payload: {e}")
        return

    issue = payload.get("issue", {})
    repo = payload.get("repository", {})

    issue_number = issue.get("number")
    issue_title = issue.get("title", "No title")
    issue_body = issue.get("body", "No description")
    owner = repo.get("owner", {}).get("login")
    repo_name = repo.get("name")

    logger.info(f"Handling edited issue #{issue_number} in {owner}/{repo_name}")

    # Generate updated analysis
    analysis = ai_service.analyze_issue(issue_title, issue_body)

    if not analysis:
        logger.error(f"Failed to generate analysis for issue #{issue_number}")
        return

    # Check if we already have a comment
    existing_comment = find_bot_comment(owner, repo_name, issue_number, ISSUE_ANALYSIS_MARKER)

    comment_body = f"{ISSUE_ANALYSIS_MARKER}\n\n{analysis}\n\n---\n*Updated: Issue was edited*"

    if existing_comment:
        # Update existing comment
        comment_id = existing_comment.get("id")
        result = update_comment(owner, repo_name, comment_id, comment_body)
        if result:
            logger.info(f"Successfully updated analysis for issue #{issue_number}")
        else:
            logger.error(f"Failed to update analysis for issue #{issue_number}")
    else:
        # Post new comment
        result = post_comment(owner, repo_name, issue_number, comment_body)
        if result:
            logger.info(f"Successfully posted analysis for issue #{issue_number}")
        else:
            logger.error(f"Failed to post analysis for issue #{issue_number}")


def handle_issue_event(payload: Dict[str, Any]) -> None:
    """
    Main handler for issue events.

    Args:
        payload: GitHub webhook payload
    """
    action = payload.get("action")

    if action == "opened":
        handle_issue_opened(payload)
    elif action == "edited":
        handle_issue_edited(payload)
    elif action == "reopened":
        handle_issue_opened(payload)
    else:
        logger.info(f"Ignoring issue action: {action}")
