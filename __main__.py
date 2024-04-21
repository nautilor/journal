#!/usr/bin/env python3
import os
import re
import json
import string
import random
import pyrogram
import argparse
import subprocess
from pyrogram.enums import ParseMode
from datetime import datetime, timedelta
from dotenv import load_dotenv as dotenv

JOURNAL_FILE = "~/.config/journal/journal.json"
DATE_FORMAT = "%d/%m/%Y"
CHANNEL_ID = 'CHANNEL_ID'
API_HASH = 'API_HASH'
API_ID = 'API_ID'


def init():
    """Load .env file with various configurations"""
    global JOURNAL_FILE, DATE_FORMAT
    global CHANNEL_ID, API_HASH, API_ID
    dotenv()
    JOURNAL_FILE = os.path.expanduser(os.getenv("JOURNAL_FILE", JOURNAL_FILE))
    DATE_FORMAT = os.getenv("DATE_FORMAT", DATE_FORMAT)
    CHANNEL_ID = os.getenv("CHANNEL_ID")
    API_HASH = os.getenv("API_HASH")
    API_ID = os.getenv("API_ID")

def create_session():
    app = pyrogram.Client("journal", API_ID, API_HASH)
    app.start()
    return app

def send_message(app, date, content):
    message = f"**Data:** __{date}__\n\n{content}"
    app.send_message(CHANNEL_ID, message, parse_mode=ParseMode.MARKDOWN)

def parse_message(message):
    date = message.split("\n")[0].split(":")[1].strip()
    content = "\n".join(message.split("\n")[2:])
    return date, content

def update_journal(app):
    messages = app.get_chat_history(CHANNEL_ID)
    for message in messages:
        if message.text:
            date, content = parse_message(message.text)
            # TODO: Update journal with content

def create_config():
    """Create configuration directory and file if they don't exist."""
    directory = os.path.dirname(JOURNAL_FILE)
    os.makedirs(directory, exist_ok=True)
    if not os.path.exists(JOURNAL_FILE):
        with open(JOURNAL_FILE, 'w') as file:
            file.write("[]")

def generate_random_id(length=24):
    """Generate a random ID."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def store_journal(element):
    """Store journal data in the JSON file."""
    with open(JOURNAL_FILE, 'r') as file:
        data = json.load(file)  
    if isinstance(data, list):
        data.append(element)
    else:
        print("Error: JSON data is not a list.")
        return 
    with open(JOURNAL_FILE, 'w') as file:
        json.dump(data, file, indent=4)

def parse_date(date_str):
    """
    Parse the given date string.

    If no date string is provided, returns the current date in custom format format.
    If the date string is 'yesterday', returns yesterday's date.
    If the date string is 'today', returns today's date.
    If the date string is 'tomorrow', returns tomorrow's date.
    Otherwise, returns the given date string as is.

    Args:
        date_str (str): The date string to parse.

    Returns:
        str: Parsed date string.
    """
    if not date_str:
        return datetime.now().strftime(DATE_FORMAT)
    elif date_str.lower() == 'yesterday':
        return (datetime.now() - timedelta(days=1)).strftime(DATE_FORMAT)
    elif date_str.lower() == 'today':
        return datetime.now().strftime(DATE_FORMAT)
    elif date_str.lower() == 'tomorrow':
        return (datetime.now() + timedelta(days=1)).strftime(DATE_FORMAT)
    else:
        return date_str

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
    create_config()
    args = parse_args()
    custom_date = parse_date(args.date)
    journal_id = generate_random_id()
    text_args = create_journal()
    data = {"id": journal_id, "date": custom_date, "content": text_args}
    store_journal(data)
    app = create_session()
    send_message(app, custom_date, text_args)

# Entry point of the script
if __name__ == "__main__":
    init()
    main()