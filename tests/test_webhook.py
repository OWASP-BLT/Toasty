"""Tests for webhook handler."""

import json
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from toasty.api.app import app
from toasty.config import settings

client = TestClient(app)


@pytest.fixture
def valid_signature():
    """Mock valid signature verification."""
    with patch("toasty.api.app.verify_signature", return_value=True):
        yield


def test_health_check():
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["app"] == settings.app_name


def test_root_endpoint():
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data


def test_webhook_missing_signature():
    """Test webhook with missing signature."""
    payload = {"action": "opened"}
    response = client.post(
        "/webhook",
        json=payload,
        headers={"X-GitHub-Event": "pull_request"},
    )
    assert response.status_code == 403


def test_webhook_invalid_signature():
    """Test webhook with invalid signature."""
    with patch("toasty.api.app.verify_signature", return_value=False):
        payload = {"action": "opened"}
        response = client.post(
            "/webhook",
            json=payload,
            headers={
                "X-GitHub-Event": "pull_request",
                "X-Hub-Signature-256": "sha256=invalid",
            },
        )
        assert response.status_code == 403


def test_webhook_empty_body():
    """Test webhook with empty body."""
    response = client.post(
        "/webhook",
        content=b"",
        headers={
            "X-GitHub-Event": "pull_request",
            "X-Hub-Signature-256": "sha256=test",
        },
    )
    assert response.status_code == 400


def test_webhook_invalid_json(valid_signature):
    """Test webhook with invalid JSON."""
    response = client.post(
        "/webhook",
        content=b"not json",
        headers={
            "X-GitHub-Event": "pull_request",
            "X-Hub-Signature-256": "sha256=test",
        },
    )
    assert response.status_code == 400


def test_webhook_ping_event(valid_signature):
    """Test webhook ping event."""
    payload = {"zen": "Test message"}
    response = client.post(
        "/webhook",
        json=payload,
        headers={
            "X-GitHub-Event": "ping",
            "X-Hub-Signature-256": "sha256=test",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "pong"
    assert data["zen"] == "Test message"


def test_webhook_missing_event_header(valid_signature):
    """Test webhook with missing event header."""
    payload = {"action": "opened"}
    response = client.post(
        "/webhook",
        json=payload,
        headers={"X-Hub-Signature-256": "sha256=test"},
    )
    assert response.status_code == 400


@patch("toasty.api.app.handle_pr_event")
def test_webhook_pull_request_event(mock_handler, valid_signature):
    """Test webhook pull request event."""
    payload = {
        "action": "opened",
        "pull_request": {"number": 1},
        "repository": {"full_name": "test/repo"},
    }
    response = client.post(
        "/webhook",
        json=payload,
        headers={
            "X-GitHub-Event": "pull_request",
            "X-Hub-Signature-256": "sha256=test",
        },
    )
    assert response.status_code == 200
    mock_handler.assert_called_once()


@patch("toasty.api.app.handle_issue_event")
def test_webhook_issue_event(mock_handler, valid_signature):
    """Test webhook issue event."""
    payload = {
        "action": "opened",
        "issue": {"number": 1},
        "repository": {"full_name": "test/repo"},
    }
    response = client.post(
        "/webhook",
        json=payload,
        headers={
            "X-GitHub-Event": "issues",
            "X-Hub-Signature-256": "sha256=test",
        },
    )
    assert response.status_code == 200
    mock_handler.assert_called_once()


@patch("toasty.api.app.handle_comment_event")
def test_webhook_comment_event(mock_handler, valid_signature):
    """Test webhook comment event."""
    payload = {
        "action": "created",
        "comment": {"body": "test"},
        "issue": {"number": 1},
        "repository": {"full_name": "test/repo"},
    }
    response = client.post(
        "/webhook",
        json=payload,
        headers={
            "X-GitHub-Event": "issue_comment",
            "X-Hub-Signature-256": "sha256=test",
        },
    )
    assert response.status_code == 200
    mock_handler.assert_called_once()


def test_webhook_unsupported_event(valid_signature):
    """Test webhook with unsupported event type."""
    payload = {"action": "opened"}
    response = client.post(
        "/webhook",
        json=payload,
        headers={
            "X-GitHub-Event": "push",
            "X-Hub-Signature-256": "sha256=test",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert "ignored" in data["status"].lower()
