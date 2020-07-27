# DiscordBot.py
from exceptions.BotException import BotException
from websockets.exceptions import InvalidStatusCode
from commands.CommandRunner import CommandRunner
from commands.character.SignupCharacterCommand import SignupCharacterCommand
from utils.Constants import MAINTAINER_ID
from utils.EmojiNames import EMOJI_SIGNUP_STATUS
from client.RaidEventsResource import RaidEventsResource
from client.PlayersResource import PlayersResource
from client.GuildsResource import GuildsResource
from client.MessagesResource import MessagesResource
from dotenv import load_dotenv

import utils.Logger as Log
import discord
import logging
import os
import traceback

maintainer = None


def run() -> None:
    os.environ['TZ'] = 'Europe/Brussels'
    load_dotenv()
    Log.setup()

    token = os.getenv('DISCORD_TOKEN')
    assert token, "Could not find any discord token"

    discord_client = discord.Client()
    players_resource = PlayersResource()
    guilds_resource = GuildsResource(discord_client)
    messages_resource = MessagesResource()
    events_resource = RaidEventsResource(discord_client, messages_resource)
    command_runner = CommandRunner(client=discord_client, players_resource=players_resource, events_resource=events_resource, guilds_resource=guilds_resource,
                                   messages_resource=messages_resource)

    @discord_client.event
    async def on_ready() -> None:
        logging.getLogger().info(f'{discord_client.user} has connected.')

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
        if isinstance(ex, BotException):
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
