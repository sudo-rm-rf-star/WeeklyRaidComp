# bot.py
from disc.commands import make_roster, save_raids
from disc.logger import _setup_logger

import discord
from dotenv import load_dotenv
import logging
import os


def run():
    load_dotenv()
    _setup_logger()

    token = os.getenv('DISCORD_TOKEN')
    client = discord.Client()

    @client.event
    async def on_ready():
        logging.getLogger().info(f'{client.user} has connected.')

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

        commands = {
            '!makeRoster': make_roster,
            '!saveRaids': save_raids,
        }

        msg_content = message.content.strip()
        argv = msg_content.strip().split(' ')
        command_name = argv[0]

        if command_name in commands.keys():
            logging.getLogger().info(f'Received message from {message.author}:  {message.content}')
            response = await commands[command_name](client, message, *argv[1:])
            if response:
                await message.author.send(response)

    client.run(token)
