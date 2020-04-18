# Bot.py
from src.disc.Commands import make_roster, post_raid_info, show_roster, unsupported, accept_player, bench_player, remove_player
from src.disc.CommandUtils import officer_rank, anyone
from src.disc.ServerUtils import get_user
import src.disc.Logger as Log
from src.exceptions.InvalidCommandException import InvalidCommandException
from src.exceptions.BotException import BotException
from src.common.Constants import MAINTAINER

import discord
from dotenv import load_dotenv
import logging
import os
import traceback

commands = {
    '!roster': {
        'create': (make_roster, officer_rank),
        'bench': (bench_player, officer_rank),
        'accept': (accept_player, officer_rank),
        'remove': (remove_player, officer_rank),
        'show': (show_roster, anyone),
        'upcoming': (unsupported, anyone),
        'help': (unsupported, anyone)
    },
    '!raidinfo': {
        'post': (post_raid_info, officer_rank)
    },
    '!dokhelp': {
        '': (unsupported, anyone)
    }
}


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
            msg_content = message.content.strip()
            argv = msg_content.strip().split(' ')
            command = find_command(argv)
            if command:
                await execute_command(client, message, command, argv)
        except BotException as e:
            Log.error(f"{message.author}, {message.content}, {e}, {traceback.print_exc()}")
            await message.author.send(e.message)
        except Exception as e:
            Log.error(f"{message.author}, {message.content}, {e}, {traceback.print_exc()}")
            await get_user(client, MAINTAINER).send(str(e))

    client.run(token)


def find_command(argv):
    command = argv[0]
    if command in commands:
        subcommand = argv[1]
        if subcommand not in commands[command]:
            raise InvalidCommandException(f"Invalid subcommand {subcommand}")
        return commands[command][subcommand]
    return None


async def execute_command(client, message, command, argv):
    await message.delete()
    command, authority_check = command
    authority_check(client, message.author)
    await command(client, message, ' '.join(argv[2:]))
