"""Validation utilities for webhook payloads."""

import json
import logging
from pathlib import Path
from typing import Any, Dict

from jsonschema import ValidationError, validate

logger = logging.getLogger(__name__)

SCHEMA_DIR = Path(__file__).parent.parent / "schemas"


def load_schema(schema_name: str) -> Dict[str, Any]:
    """
    Load a JSON schema file.

    Args:
        schema_name: Name of the schema file (e.g., 'pr_schema.json')

    Returns:
        Loaded schema dictionary

    Raises:
        FileNotFoundError: If schema file doesn't exist
        json.JSONDecodeError: If schema file is invalid JSON
    """
    schema_path = SCHEMA_DIR / schema_name
    with open(schema_path, "r", encoding="utf-8") as f:
        return json.load(f)


def validate_payload(payload: Dict[str, Any], schema: Dict[str, Any]) -> bool:
    """
    Validate a webhook payload against a JSON schema.

    Args:
        payload: The webhook payload to validate
        schema: The JSON schema to validate against

    Returns:
        True if validation succeeds

    Raises:
        ValidationError: If payload doesn't conform to schema
    """
    try:
        validate(instance=payload, schema=schema)
        return True
    except ValidationError as e:
        logger.error(f"Payload validation failed: {e.message}")
        raise


def validate_pr_payload(payload: Dict[str, Any]) -> bool:
    """Validate pull request webhook payload."""
    schema = load_schema("pr_schema.json")
    return validate_payload(payload, schema)


def validate_issue_payload(payload: Dict[str, Any]) -> bool:
    """Validate issue webhook payload."""
    schema = load_schema("issue_schema.json")
    return validate_payload(payload, schema)


def validate_comment_payload(payload: Dict[str, Any]) -> bool:
    """Validate comment webhook payload."""
    schema = load_schema("comment_schema.json")
    return validate_payload(payload, schema)
