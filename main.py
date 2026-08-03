#!/usr/bin/env python3
"""
Entry point for running either the Flask or FastAPI task API server.
"""
import argparse
from typing import Optional

from fastapi_app import app as fastapi_app
from flask_app import app as flask_app


def run_flask(port: int) -> None:
    """Run the Flask server."""
    flask_app.run(port=port)


def run_fastapi(port: int) -> None:
    """Run the FastAPI server."""
    import uvicorn
    uvicorn.run(fastapi_app, port=port)


def parse_args(args: Optional[list[str]] = None) -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Run task API server")
    parser.add_argument(
        "--flask",
        action="store_true",
        help="use Flask server (default: FastAPI)"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="port to run server on (default: 8000)"
    )
    return parser.parse_args(args)


def main() -> None:
    """Run the selected server based on CLI arguments."""
    args = parse_args()
    if args.flask:
        run_flask(args.port)
    else:
        run_fastapi(args.port)


if __name__ == "__main__":
    main()