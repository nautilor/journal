#!/usr/bin/env python3

from os import getenv
from pyrogram import Client
from pyrogram.enums import ParseMode
from root.extension.base_extension import BaseExtension
from os.path import expanduser

class Telegram(BaseExtension):
    def __init__(self):
        super().__init__("telegram")
        self.session_file: str = expanduser(getenv("telegram_session_file", "~/.config/journal/session"))
        self.api_id: str = getenv("telegram_api_id", "")
        self.api_hash: str = getenv("telegram_api_hash", "")
        self.channel_id: str = getenv("telegram_channel_id", "")
        self.app: Client = self.create_session()
        self.app.start()

    def create_session(self) -> Client:
        return Client(self.session_file, self.api_id, self.api_hash)
    

    def execute(self, content: str, date: str):
        date = self.format_date(date)
        message = f"**Data:** __{date}__\n\n{content}"
        self.app.send_message(self.channel_id, message, parse_mode=ParseMode.MARKDOWN)