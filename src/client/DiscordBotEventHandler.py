# DiscordBot.py
from exceptions.BotException import BotException
from exceptions.InternalBotException import InternalBotException
from websockets.exceptions import InvalidStatusCode
from commands.CommandRunner import CommandRunner
from commands.character.SignupCharacterCommand import SignupCharacterCommand
from events.SQSQueue import SQSQueue
from utils.Constants import MAINTAINER_ID
from utils.EmojiNames import EMOJI_SIGNUP_STATUS
from client.RaidEventsResource import RaidEventsResource
from client.PlayersResource import PlayersResource
from client.GuildsResource import GuildsResource
from client.MessagesResource import MessagesResource
from dotenv import load_dotenv
from datetime import datetime

import utils.Logger as Log
import discord
import logging
import asyncio
import os
import sys
import traceback

maintainer = None
LOOP_INTERVAL_SECS = 10


def run() -> None:
    if sys.platform != 'win32':
        from time import tzset
        tzset()

    print(datetime.now())
    load_dotenv()
    Log.setup()

    token = os.getenv('DISCORD_BOT_TOKEN')
    assert token, "Could not find any discord bot token"

    discord_client = discord.Client()
    players_resource = PlayersResource()
    guilds_resource = GuildsResource(discord_client)
    messages_resource = MessagesResource()
    events_resource = RaidEventsResource(discord_client, messages_resource)
    command_runner = CommandRunner(client=discord_client, players_resource=players_resource, events_resource=events_resource, guilds_resource=guilds_resource,
                                   messages_resource=messages_resource)
    events_queue = SQSQueue()
    loop = discord_client.loop

    async def listen_queue():
        await events_queue.receive_messages(send_maintainer)
        loop.call_later(LOOP_INTERVAL_SECS, loop.create_task, listen_queue())

    async def send_maintainer(msg):
        global maintainer
        await maintainer.send(msg)

    @discord_client.event
    async def on_ready() -> None:
        global maintainer
        print(f'{discord_client.user} has connected.')
        maintainer = await discord_client.fetch_user(MAINTAINER_ID)
        loop.create_task(listen_queue())

    discord_client.run(token)

    @discord_client.event
    async def on_message(message: discord.Message) -> None:
        if not discord_client.is_ready() or message.author == discord_client.user:
            return
        try:
            await command_runner.run_command_for_message(message)
        except Exception as ex:
            await handle_exception(ex, author=message.author, content=message.content)

    @discord_client.event
    async def on_raw_reaction_add(reaction_event: discord.RawReactionActionEvent) -> None:
        if not discord_client.is_ready() or reaction_event.user_id == discord_client.user.id or reaction_event.emoji.name not in EMOJI_SIGNUP_STATUS.keys():
            return
        try:
            await command_runner.run_command_for_reaction_event(reaction_event, SignupCharacterCommand)
        except Exception as ex:
            user = await discord_client.fetch_user(reaction_event.user_id)
            await handle_exception(ex, author=user, content="Raid signup failed")

    async def handle_exception(ex: Exception, author: discord.User, content: str) -> None:
        Log.error(f"{author}, {content}, {ex}\n{traceback.format_exc()}")
        if isinstance(ex, BotException) and not isinstance(ex, InternalBotException):
            await author.send(ex.message)
        else:
            global maintainer
            if maintainer is None:
                maintainer = await discord_client.fetch_user(MAINTAINER_ID)
            await author.send(f"There were internal difficulties. Sending a message to {maintainer.display_name}")
            await maintainer.send(f'{author.display_name}, {content}, {ex}')

    try:
        discord_client.run(token)
    except InvalidStatusCode as e:
        error_message = f"Could not start client {e}\n{traceback.format_exc()}"
        Log.error(error_message)
