#!/usr/bin/env python3

from os import getenv
from datetime import datetime
from datetime import timedelta

class BaseExtension:
    def __init__(self, name="base_extension"):
        self.name = name
    
    def is_enabled(self) -> bool:
        """
        Check if the extension is enabled.
        """
        key: str = f"{self.name.lower()}_enabled"
        return getenv(key, "false").lower() == "true"
    
    def format_date(self, date: str) -> str:
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
        date_format = getenv("date_format", "%d/%m/%Y")
        if not date:
            return datetime.now().strftime(date_format)
        elif date.lower() == 'yesterday':
            return (datetime.now() - timedelta(days=1)).strftime(date_format)
        elif date.lower() == 'today':
            return datetime.now().strftime(date_format)
        elif date.lower() == 'tomorrow':
            return (datetime.now() + timedelta(days=1)).strftime(date_format)
        else:
            return date
    
    def execute(self, message: str, date: str):
        """
        Execute the extension.
        """
        if self.is_enabled():
            raise NotImplementedError("Method not implemented")