# DiscordBot.py
from exceptions.BotException import BotException
from websockets.exceptions import InvalidStatusCode
from commands.BotCommands import find_and_execute_command, execute_command
from commands.player.SignupPlayerCommand import SignupPlayerCommand
from utils.Constants import MAINTAINER
from utils.EmojiNames import EMOJI_SIGNUP_STATUS
from client.DiscordClient import DiscordClient
from client.RaidEventsResource import RaidEventsResource
from client.PlayersResource import PlayersResource
from dotenv import load_dotenv

import utils.Logger as Log
import discord
import logging
import os
import traceback


def run() -> None:
    load_dotenv()
    Log.setup()

    token = os.getenv('DISCORD_TOKEN')
    assert token, "Could not find any discord token"

    client = discord.Client()
    discord_client = DiscordClient(client)
    events_resource = RaidEventsResource(discord_client)
    players_resource = PlayersResource(discord_client)

    @client.event
    async def on_ready() -> None:
        await discord_client.on_ready()
        events_resource.on_ready()
        logging.getLogger().info(f'{client.user} has connected.')

    @client.event
    async def on_message(message: discord.Message) -> None:
        if not client.is_ready() or message.author == client.user:
            return
        try:
            await find_and_execute_command(discord_client, events_resource, players_resource, message=message)
        except Exception as ex:
            await handle_exception(discord_client, ex, message)

    @client.event
    async def on_raw_reaction_add(reaction_event: discord.RawReactionActionEvent) -> None:
        if not client.is_ready() or reaction_event.user_id == client.user.id or reaction_event.emoji.name not in EMOJI_SIGNUP_STATUS.keys():
            return
        try:
            await execute_command(SignupPlayerCommand(), "", discord_client, events_resource, players_resource, raw_reaction=reaction_event)
        except Exception as ex:
            member = discord_client.get_member_by_id(reaction_event.user_id)
            err_msg = f"Raid signup failed for {member}, {reaction_event.emoji}, {ex}"
            Log.error(f'{err_msg}\n{traceback.format_exc()}')
            if isinstance(ex, BotException):
                await member.send(ex.message)
            else:
                await member.send(f"There were internal difficulties. Sending a message to {MAINTAINER}")
                await discord_client.get_member(MAINTAINER).send(err_msg)

    try:
        client.run(token)
    except InvalidStatusCode as e:
        error_message = f"Could not start client {e}\n{traceback.format_exc()}"
        Log.error(error_message)


async def handle_exception(client: DiscordClient, ex: Exception, message: discord.Message) -> None:
    Log.error(f"{message.author}, {message.content}, {ex}\n{traceback.format_exc()}")
    if isinstance(ex, BotException):
        await message.author.send(ex.message)
    else:
        await message.author.send(f"There were internal difficulties. Sending a message to {MAINTAINER}")
        await client.get_member(MAINTAINER).send(f'{message.author}, {message.content}, {ex}')
