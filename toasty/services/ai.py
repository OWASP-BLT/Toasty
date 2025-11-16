"""AI service for generating code reviews and analyses."""

import logging
import random
import time
from typing import Optional

import google.generativeai as genai

from toasty.config import settings

logger = logging.getLogger(__name__)


class AIService:
    """Service for interacting with Gemini AI."""

    def __init__(self) -> None:
        """Initialize the AI service."""
        if settings.gemini_api_key:
            genai.configure(api_key=settings.gemini_api_key)
            self.model = genai.GenerativeModel(settings.gemini_model)
        else:
            logger.warning("Gemini API key not configured")
            self.model = None

    def generate_response(self, prompt: str, max_retries: Optional[int] = None) -> Optional[str]:
        """
        Generate a text response from the Gemini model with retry logic.

        Args:
            prompt: Input prompt for the AI model
            max_retries: Maximum number of retry attempts (defaults to settings.max_retries)

        Returns:
            Generated text if successful, None if failed
        """
        if not self.model:
            logger.error("AI model not initialized")
            return None

        if not prompt or not isinstance(prompt, str):
            logger.error("Invalid prompt provided")
            return None

        max_retries = max_retries or settings.max_retries

        for attempt in range(1, max_retries + 1):
            try:
                logger.info(f"Generating AI response (attempt {attempt}/{max_retries})")
                response = self.model.generate_content(prompt)

                if not response.text:
                    raise ValueError("Empty response from model")

                logger.debug("Successfully generated AI response")
                return response.text

            except Exception as e:
                logger.warning(f"AI generation error on attempt {attempt}: {e}")

                if attempt < max_retries:
                    wait_time = settings.retry_backoff * (2 ** (attempt - 1)) + random.uniform(0, 1)
                    logger.info(f"Retrying in {wait_time:.1f}s...")
                    time.sleep(wait_time)

        logger.error(f"Failed to generate AI response after {max_retries} attempts")
        return None

    def analyze_pr(self, title: str, description: str, diff: str, files: list) -> Optional[str]:
        """
        Analyze a pull request and generate a code review.

        Args:
            title: PR title
            description: PR description
            diff: PR diff content
            files: List of changed files

        Returns:
            Generated code review or None if failed
        """
        file_list = "\n".join([f"- {f.get('filename', 'unknown')}" for f in files[:20]])

        prompt = f"""You are a security-focused code reviewer for an open-source project. 
Analyze this pull request and provide a comprehensive review with a focus on:

1. **Security**: Identify potential vulnerabilities, security risks, or unsafe practices
2. **Code Quality**: Check for bugs, anti-patterns, and maintainability issues
3. **Best Practices**: Ensure the code follows language-specific best practices
4. **Performance**: Identify potential performance issues
5. **Testing**: Assess test coverage and quality

Pull Request Details:
Title: {title}
Description: {description or "No description provided"}

Changed Files:
{file_list}

Code Diff (first 3000 chars):
{diff[:3000]}

Provide your review in the following format:
- Start with an overall assessment (APPROVE, REQUEST CHANGES, or COMMENT)
- List specific issues found with file names and line numbers
- Highlight any security concerns
- Suggest improvements
- Keep it concise and actionable

Generate the review:"""

        return self.generate_response(prompt)

    def analyze_issue(self, title: str, body: str) -> Optional[str]:
        """
        Analyze a GitHub issue and provide insights.

        Args:
            title: Issue title
            body: Issue body/description

        Returns:
            Generated analysis or None if failed
        """
        prompt = f"""You are an AI assistant helping with GitHub issue triage and analysis.

Issue Title: {title}
Issue Description: {body or "No description provided"}

Your task:
1. Categorize the issue (bug, feature request, question, documentation, etc.)
2. Assess the issue's priority and severity
3. Identify if it's a security-related issue
4. Suggest appropriate labels
5. Ask clarifying questions if the issue is unclear
6. Provide helpful initial guidance or resources

Keep your response concise, friendly, and professional.

Generate your analysis:"""

        return self.generate_response(prompt)

    def respond_to_comment(self, comment: str, context: str) -> Optional[str]:
        """
        Generate a response to a comment mentioning the bot.

        Args:
            comment: The comment text
            context: Additional context (PR/issue details)

        Returns:
            Generated response or None if failed
        """
        prompt = f"""You are a helpful GitHub bot assistant. Respond to this comment in a professional and helpful manner.

Context: {context}
Comment: {comment}

Your response should:
1. Address the specific question or request
2. Provide actionable advice
3. Be concise and friendly
4. Include relevant links or documentation if applicable

Generate your response:"""

        return self.generate_response(prompt)


# Global AI service instance
ai_service = AIService()
