"""Main entry point for Toasty bot."""

import uvicorn

from toasty.config import settings


def main() -> None:
    """Run the Toasty bot server."""
    uvicorn.run(
        "toasty.api.app:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level="debug" if settings.debug else "info",
    )


if __name__ == "__main__":
    main()
