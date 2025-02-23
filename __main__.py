#!/usr/bin/env python3
import os
import subprocess
from dotenv import load_dotenv as dotenv
from telethon import TelegramClient
import asyncio
from telethon.tl.types import PeerChannel

class Journal:
    app: TelegramClient = None
    channel_id: str = None
    api_hash: str = None
    api_id: str = None

    async def initialize(self):
        """Load .env file with various configurations"""
        dotenv()
        self.channel_id = os.getenv("CHANNEL_ID")
        self.api_hash = os.getenv("API_HASH")
        self.api_id = os.getenv("API_ID")
        await self.create_session()
    
    async def create_session(self):
        if not self.api_id or not self.api_hash:
            print("Please provide a valid API ID and API hash.")
            exit(-1)
        self.app = TelegramClient('journal', self.api_id, self.api_hash)
        self.app.parse_mode = 'md'
        await self.app.start()
    
    async def send_message(self, content: str):
        message = f"{content}"
        if not self.channel_id:
            print("Please provide a valid channel ID.")
            exit(-1)
        entity = await self.app.get_entity(PeerChannel(int(self.channel_id)))
        await self.app.send_message(entity, message)


    def create_journal(self):
        """Create a journal entry using the default text editor."""
        try:
            editor = os.environ.get("EDITOR", "vim")
            subprocess.run([editor, "/tmp/journal.md"])

            with open("/tmp/journal.md", "r") as file:
                text = file.read()

            subprocess.run(["rm", "/tmp/journal.md"])
            return text
        except FileNotFoundError:
            exit()

async def main():
    journal: Journal = Journal()
    await journal.initialize()
    text: str = journal.create_journal()
    await journal.send_message(text)

# Entry point of the script
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
