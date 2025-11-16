"""Configuration management for Toasty bot."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # GitHub Configuration
    github_token: str = ""
    github_webhook_secret: str = ""
    github_api_url: str = "https://api.github.com"
    github_bot_username: str = "toasty-bot"

    # AI Configuration
    gemini_api_key: str = ""
    gemini_model: str = "gemini-2.0-flash"

    # Application Configuration
    app_name: str = "Toasty"
    app_version: str = "0.1.0"
    debug: bool = False
    host: str = "0.0.0.0"
    port: int = 8000

    # Webhook Configuration
    webhook_path: str = "/webhook"
    health_check_path: str = "/health"

    # Retry Configuration
    max_retries: int = 5
    retry_backoff: int = 2

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


settings = Settings()
