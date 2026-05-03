"""Command-line entry point for Lab 4."""
from __future__ import annotations

import argparse

from lab4_application import Lab4Application


def main() -> None:
    parser = argparse.ArgumentParser(description="Lab 4: Strategy-based dataset export")
    parser.add_argument(
        "--config",
        default="lab4_config.json",
        help="Path to the JSON configuration file",
    )
    args = parser.parse_args()

    app = Lab4Application(args.config)
    app.run()


if __name__ == "__main__":
    main()

