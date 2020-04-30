# DiscordBot.py
from src.client.GuildClient import GuildClient
from src.exceptions.BotException import BotException
from src.common.Constants import MAINTAINER, GUILD
from src.commands.BotCommands import find_and_execute_command
from src.commands.utils.RaidSignup import raid_signup
from typing import Union
from dotenv import load_dotenv

import src.client.Logger as Log
import discord
import logging
import os
import traceback

client_wrapper = None


def run() -> None:
    load_dotenv()
    Log.setup()

    token = os.getenv('DISCORD_TOKEN')
    client = discord.Client()

    @client.event
    async def on_ready() -> None:
        global client_wrapper
        guilds = await client.fetch_guilds().flatten()
        guild = discord.utils.get(guilds, name=GUILD)
        guild = client.get_guild(guild.id)
        client_wrapper = GuildClient(client, guild)
        logging.getLogger().info(f'{client.user} has connected.')

    @client.event
    async def on_message(message: discord.Message) -> None:
        if not client_wrapper or message.author == client.user:
            return
        try:
            await find_and_execute_command(client_wrapper, message)
        except Exception as e:
            Log.error(f"{message.author}, {message.content}, {e}\n{traceback.format_exc()}")
            if isinstance(e, BotException):
                await message.author.send(e.message)
            else:
                await message.author.send(f"There were internal difficulties. Sending a message to {MAINTAINER}")
                await client_wrapper.get_member(MAINTAINER).send(f'{message.author}, {message.content}, {e}')

    @client.event
    async def on_raw_reaction_add(reaction_event: discord.RawReactionActionEvent) -> None:
        if not client_wrapper or reaction_event.user_id == client.user.id:
            return
        await raid_signup(client_wrapper, reaction_event.user_id, reaction_event.message_id, reaction_event.channel_id, reaction_event.emoji)

    client.run(token)
