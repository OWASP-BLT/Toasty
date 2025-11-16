#!/usr/bin/env python3
"""Test script to send sample webhook payloads to the bot."""

import hashlib
import hmac
import json
import sys
from pathlib import Path

import requests

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from toasty.config import settings


def sign_payload(payload: dict, secret: str) -> str:
    """Generate HMAC signature for payload."""
    payload_bytes = json.dumps(payload).encode()
    mac = hmac.new(secret.encode(), payload_bytes, hashlib.sha256)
    return f"sha256={mac.hexdigest()}"


def send_webhook(event_type: str, payload: dict, url: str = None) -> None:
    """Send a webhook to the bot."""
    url = url or f"http://{settings.host}:{settings.port}{settings.webhook_path}"
    
    signature = sign_payload(payload, settings.github_webhook_secret)
    
    headers = {
        "X-GitHub-Event": event_type,
        "X-Hub-Signature-256": signature,
        "Content-Type": "application/json",
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")


def test_ping():
    """Test ping event."""
    print("\n=== Testing Ping Event ===")
    payload = {"zen": "Keep it simple, stupid."}
    send_webhook("ping", payload)


def main():
    """Run all tests."""
    print(f"Testing webhook at: http://{settings.host}:{settings.port}{settings.webhook_path}")
    print(f"Bot username: {settings.github_bot_username}")
    
    if not settings.github_webhook_secret:
        print("ERROR: GITHUB_WEBHOOK_SECRET not set in environment")
        sys.exit(1)
    
    test_ping()
    print("\n=== All tests completed ===")


if __name__ == "__main__":
    main()
