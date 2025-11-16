#!/usr/bin/env python3
"""
Quick launcher for interactive application generation
This is a convenience script to launch the interactive CLI
"""

import sys
from interactive_cli import InteractiveCLI


if __name__ == "__main__":
    cli = InteractiveCLI()
    sys.exit(cli.run())
