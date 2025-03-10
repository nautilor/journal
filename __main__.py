#!/usr/bin/env python3
import os
import subprocess
from dotenv import load_dotenv as dotenv
from telethon import TelegramClient
from telethon.tl.types import PeerChannel

class Journal:
    app: TelegramClient = None
    channel_id: None | str = None
    api_hash: None | str = None
    api_id: None | str = None

    def initialize(self):
        """Load .env file with various configurations"""
        dotenv()
        self.channel_id = os.getenv("CHANNEL_ID")
        self.api_hash = os.getenv("API_HASH")
        self.api_id = os.getenv("API_ID")
        if not self.api_id or not self.api_hash:
            print("Please provide a valid API ID and API Hash.")
            exit(-1)
        self.create_session()
    
    def create_session(self):
        current_path: str = os.path.dirname(os.path.realpath(__file__))
        self.app = TelegramClient(f'{current_path}/journal', self.api_id, self.api_hash)
        self.app.parse_mode = 'md'
    
    async def connect(self):
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

async def main(journal: Journal):
    await journal.connect()
    text: str = journal.create_journal()
    await journal.send_message(text)

# Entry point of the script
if __name__ == "__main__":
    journal: Journal = Journal()
    journal.initialize()
    journal.app.loop.run_until_complete(main(journal))
