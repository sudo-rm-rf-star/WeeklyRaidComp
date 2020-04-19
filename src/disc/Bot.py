# Bot.py
from src.disc.ServerUtils import get_user
import src.disc.Logger as Log
from src.exceptions.BotException import BotException
from src.common.Constants import MAINTAINER
from src.commands.BotCommands import find_and_execute_command

import discord
from dotenv import load_dotenv
import logging
import os
import traceback


def run():
    load_dotenv()
    Log.setup()

    token = os.getenv('DISCORD_TOKEN')
    client = discord.Client()

    @client.event
    async def on_ready():
        logging.getLogger().info(f'{client.user} has connected.')

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return
        try:
            await find_and_execute_command(client, message)
        except Exception as e:
            Log.error(f"{message.author}, {message.content}, {e}\n{traceback.format_exc()}")
            if isinstance(e, BotException):
                await message.author.send(e.message)
            else:
                await message.author.send(f"There were internal difficulties. Sending a message to {MAINTAINER}")
                await get_user(client, MAINTAINER).send(f'{message.author}, {message.content}, {e}')

    client.run(token)
