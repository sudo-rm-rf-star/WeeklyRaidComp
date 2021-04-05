# BotSetup.py
from websockets.exceptions import InvalidStatusCode
from dokbot.DokBotCog import DokBotCog
from events.EventCog import EventCog
from dotenv import load_dotenv
from datetime import datetime
from .DokBot import DokBot

import utils.Logger as Log
import logging
import os
import sys
import traceback
import discord


def run() -> None:
    os.environ['TZ'] = 'Europe/Brussels'
    if sys.platform != 'win32':
        from time import tzset
        tzset()

    print(datetime.now())
    load_dotenv()
    Log.setup()

    token = os.getenv('DISCORD_BOT_TOKEN')
    assert token, "Could not find any dokbot bot token"

    intents = discord.Intents.default()
    intents.members = True

    prefix = '>' if os.getenv('APP_ENV') == 'development' else '!'
    bot = DokBot(command_prefix=prefix, intents=intents)
    bot.add_cog(DokBotCog(bot))
    bot.add_cog(EventCog(bot))

    @bot.event
    async def on_ready():
        logging.getLogger().info(f'{bot.user.name} has connected.')

    #
    # @discord_client.event
    # async def on_message(message: discord.Message) -> None:
    #     if not discord_client.is_ready() or message.author == discord_client.user:
    #         return
    #     try:
    #         await command_runner.run_command_for_message(message)
    #     except Exception as ex:
    #         await handle_exception(ex, author=message.author, content=message.content)
    #
    # @discord_client.event
    # async def on_raw_reaction_add(reaction_event: discord.RawReactionActionEvent) -> None:
    #     if not discord_client.is_ready() or reaction_event.user_id == discord_client.user.id or reaction_event.emoji.name not in EMOJI_SIGNUP_STATUS.keys():
    #         return
    #     try:
    #         await signup_character(client=discord_client, reaction_event=reaction_event)
    #     except Exception as ex:
    #         user = await discord_client.fetch_user(reaction_event.user_id)
    #         await handle_exception(ex, author=user, content="Raid signup failed")
    #
    # async def handle_exception(ex: Exception, author: discord.User, content: str) -> None:
    #     Log.error(f"{author}, {content}, {ex}\n{traceback.format_exc()}")
    #     if isinstance(ex, BotException) and not isinstance(ex, InternalBotException):
    #         await author.send(ex.message)
    #     else:
    #         global maintainer
    #         if maintainer is None:
    #             maintainer = await discord_client.fetch_user(MAINTAINER_ID)
    #         await author.send(f"There were internal difficulties. Sending a message to {maintainer.display_name}")
    #         await maintainer.send(f'{author.display_name}, {content}, {ex}')
    #
    try:
        bot.run(token)
    except InvalidStatusCode as e:
        error_message = f"Could not start client {e}\n{traceback.format_exc()}"
        Log.error(error_message)
