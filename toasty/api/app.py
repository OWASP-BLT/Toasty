"""FastAPI application for Toasty bot."""

import json
import logging
from typing import Any, Dict

from fastapi import FastAPI, Header, HTTPException, Request, status
from fastapi.responses import JSONResponse

from toasty.config import settings
from toasty.handlers.comment_handler import handle_comment_event
from toasty.handlers.issue_handler import handle_issue_event
from toasty.handlers.pr_handler import handle_pr_event
from toasty.utils.github import verify_signature

logging.basicConfig(
    level=logging.INFO if not settings.debug else logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="GitHub bot for AI code reviews, project management, and security analysis",
)


@app.get(settings.health_check_path)
async def health_check() -> Dict[str, str]:
    """
    Health check endpoint.

    Returns:
        Status information
    """
    return {
        "status": "healthy",
        "app": settings.app_name,
        "version": settings.app_version,
    }


@app.post(settings.webhook_path)
async def webhook_handler(
    request: Request,
    x_github_event: str = Header(None),
    x_hub_signature_256: str = Header(None),
) -> JSONResponse:
    """
    Main webhook handler for GitHub events.

    Args:
        request: FastAPI request object
        x_github_event: GitHub event type header
        x_hub_signature_256: GitHub signature header

    Returns:
        JSON response indicating success or failure
    """
    # Read request body
    try:
        body = await request.body()
        if not body:
            logger.warning("Empty request body received")
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Empty request body")
    except Exception as e:
        logger.error(f"Failed to read request body: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid request")

    # Verify signature
    if not x_hub_signature_256:
        logger.warning("Missing signature header")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Missing signature header")

    if not verify_signature(body, x_hub_signature_256):
        logger.warning("Invalid signature")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid signature")

    # Parse JSON payload
    try:
        payload: Dict[str, Any] = json.loads(body)
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON payload: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid JSON")

    # Check event type header
    if not x_github_event:
        logger.warning("Missing event type header")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Missing event type header")

    # Log event
    action = payload.get("action", "unknown")
    logger.info(f"Received webhook - Event: {x_github_event}, Action: {action}")

    # Handle ping event
    if x_github_event == "ping":
        zen = payload.get("zen", "No zen message")
        logger.info(f"Webhook ping received: {zen}")
        return JSONResponse(content={"status": "pong", "zen": zen})

    # Route to appropriate handler
    try:
        if x_github_event == "pull_request":
            handle_pr_event(payload)
            return JSONResponse(content={"status": "Pull request event processed"})
        elif x_github_event == "issues":
            handle_issue_event(payload)
            return JSONResponse(content={"status": "Issue event processed"})
        elif x_github_event == "issue_comment":
            handle_comment_event(payload)
            return JSONResponse(content={"status": "Comment event processed"})
        else:
            logger.info(f"Unsupported event type: {x_github_event}")
            return JSONResponse(content={"status": "Unsupported event type - ignored"})
    except Exception as e:
        logger.error(f"Error processing webhook: {e}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@app.get("/")
async def root() -> Dict[str, str]:
    """
    Root endpoint.

    Returns:
        Welcome message
    """
    return {
        "message": f"Welcome to {settings.app_name}",
        "version": settings.app_version,
        "webhook_url": settings.webhook_path,
    }
