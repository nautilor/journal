#!/usr/bin/env python3
from root.extension.telegram import Telegram

extensions = [Telegram]

def load_extensions():
    """
    Load all extensions.
    """
    return [e() for e in extensions]