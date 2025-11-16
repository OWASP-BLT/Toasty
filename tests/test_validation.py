"""Tests for payload validation."""

import pytest
from jsonschema import ValidationError

from toasty.utils.validation import validate_comment_payload, validate_issue_payload, validate_pr_payload


def test_validate_pr_payload_valid():
    """Test validation of valid PR payload."""
    payload = {
        "action": "opened",
        "pull_request": {
            "number": 1,
            "title": "Test PR",
            "body": "Test body",
            "user": {"login": "testuser", "type": "User"},
        },
        "repository": {
            "full_name": "test/repo",
            "owner": {"login": "test"},
            "name": "repo",
        },
    }
    assert validate_pr_payload(payload) is True


def test_validate_pr_payload_missing_field():
    """Test validation of PR payload with missing field."""
    payload = {
        "action": "opened",
        "pull_request": {
            "number": 1,
            # Missing title
            "user": {"login": "testuser", "type": "User"},
        },
        "repository": {
            "full_name": "test/repo",
            "owner": {"login": "test"},
            "name": "repo",
        },
    }
    with pytest.raises(ValidationError):
        validate_pr_payload(payload)


def test_validate_issue_payload_valid():
    """Test validation of valid issue payload."""
    payload = {
        "action": "opened",
        "issue": {
            "number": 1,
            "title": "Test Issue",
            "body": "Test body",
            "user": {"login": "testuser", "type": "User"},
        },
        "repository": {
            "full_name": "test/repo",
            "owner": {"login": "test"},
            "name": "repo",
        },
    }
    assert validate_issue_payload(payload) is True


def test_validate_comment_payload_valid():
    """Test validation of valid comment payload."""
    payload = {
        "action": "created",
        "comment": {
            "id": 123,
            "body": "Test comment",
            "user": {"login": "testuser", "type": "User"},
        },
        "issue": {"number": 1},
        "repository": {
            "full_name": "test/repo",
            "owner": {"login": "test"},
            "name": "repo",
        },
    }
    assert validate_comment_payload(payload) is True
