#!/usr/bin/env python3
from dotenv import load_dotenv as dotenv
import os
from os.path import expanduser

CONFIGURATION_FILE = expanduser("~/.config/journal/configuration")

def load_configuration():
    create_configuration()
    dotenv(CONFIGURATION_FILE)

def create_configuration():
    """Create configuration directory and file if they don't exist."""
    directory = os.path.dirname(CONFIGURATION_FILE)
    os.makedirs(directory, exist_ok=True)
    if not os.path.exists(CONFIGURATION_FILE):
        with open(CONFIGURATION_FILE, 'w') as file:
            file.write("")