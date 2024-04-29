#!/usr/bin/env python3
import os
import argparse
import subprocess
from root.tools.configuration import load_configuration
from root.extension.extensions import load_extensions

def parse_args():
    """
    Parse command-line arguments.

    Returns:
        argparse.Namespace: Parsed arguments.
    """
    parser = argparse.ArgumentParser(description='Process arguments.')
    parser.add_argument('-d', '--date', help='Custom date')
    return parser.parse_args()

def create_journal():
    """Create a journal entry using the default text editor."""
    try:
        editor = os.environ.get("EDITOR", "vim")
        subprocess.run([editor, "/tmp/journal.tmp"])

        with open("/tmp/journal.tmp", "r") as file:
            text = file.read()

        subprocess.run(["rm", "/tmp/journal.tmp"])

        return text
    except FileNotFoundError:
        exit()

def main():
    """Execute the main functionality of the script."""
    load_configuration()
    args = parse_args()
    date = args.date
    content = create_journal()
    extensions = load_extensions()
    [e.execute(content, date) for e in extensions if e.is_enabled()]

# Entry point of the script
if __name__ == "__main__":
    main()