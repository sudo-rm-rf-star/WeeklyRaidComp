"""File full of magic to avoid relying on every single BotCommand"""
from commands.BotCommand import BotCommand
from exceptions.InvalidCommandException import InvalidCommandException
from collections import defaultdict
from setuptools import find_packages
from pkgutil import iter_modules
from typing import Set, Dict
from pathlib import Path
import importlib
import discord
import sys
from client.RaidEventsResource import RaidEventsResource
from client.PlayersResource import PlayersResource
from client.GuildsResource import GuildsResource
from typing import Optional
import utils.Logger as Log


def find_modules(path: str) -> Set[str]:
    modules = set()
    for pkg in find_packages(path):
        modules.add(pkg)
        pkgpath = path + '/' + pkg.replace('.', '/')
        if sys.version_info.major == 2 or (sys.version_info.major == 3 and sys.version_info.minor < 6):
            for _, name, ispkg in iter_modules([pkgpath]):
                if not ispkg:
                    modules.add(pkg + '.' + name)
        else:
            for info in iter_modules([pkgpath]):
                if not info.ispkg:
                    modules.add(pkg + '.' + info.name)
    return modules


def _all_subclasses(cls: type) -> Set[type]:
    recursive_subclasses = set()
    if len(cls.__subclasses__()) > 0:
        for subclass in cls.__subclasses__():
            for r_subclass in _all_subclasses(subclass):
                recursive_subclasses.add(r_subclass)
    else:  # Max recursion
        recursive_subclasses.add(cls)

    return recursive_subclasses


def _get_bot_commands() -> Dict[str, Dict[str, BotCommand]]:
    bot_commands = defaultdict(dict)
    for command_cls in _all_subclasses(BotCommand):
        try:
            command = command_cls()
            bot_commands[command.name][command.subname] = command
        except TypeError:
            Log.error(f'Could not initialize {command_cls}')

    return dict(bot_commands)


async def find_bot_command(message: Optional[discord.Message], command_name: str, subcommand_name: str) -> BotCommand:
    command_prefix = command_name[0]
    command_name = command_name[1:]
    if command_prefix == '!' and command_name in BOT_COMMANDS:
        if message:  # At this point we can safely delete the message as it is intended for the bot
            try:
                await message.delete()
            except discord.NotFound:  # This happens when multiple versions of the bot are running.
                pass
            except discord.Forbidden:  # This happens when users are performing actions in DM.
                pass

        # For now we do this, with the current system we have a dependency in both directions otherwise,
        if subcommand_name == 'help':
            from commands.HelpCommand import HelpCommand
            return HelpCommand(command_name)

        if subcommand_name in BOT_COMMANDS[command_name]:
            return BOT_COMMANDS[command_name][subcommand_name]
        else:
            raise InvalidCommandException(f"{command_name} {subcommand_name} is not a valid bot command.")


async def find_and_execute_command(client: discord.Client, events_resource: RaidEventsResource, players_resource: PlayersResource,
                                   guilds_resource: GuildsResource, message: Optional[discord.Message] = None,
                                   raw_reaction: Optional[discord.RawReactionActionEvent] = None) -> None:
    cmd = None
    cmd_args = None
    try:
        # Parsing here could be moved to ArgParser
        argv = message.content
        args = tuple(argv.split(' '))
        cmd_name, subcmd_name = tuple(args[:2])
        cmd_args = ' '.join(args[2:])
        cmd = await find_bot_command(message, cmd_name, subcmd_name)
    except (IndexError, ValueError):
        pass  # This is not a command intended for our bot.

    if cmd and cmd_args is not None:
        await execute_command(cmd, cmd_args, client, events_resource, players_resource, guilds_resource, message, raw_reaction)


async def execute_command(command: BotCommand, cmd_args: str, client: discord.Client, events_resource: RaidEventsResource, players_resource: PlayersResource,
                          guilds_resource: GuildsResource, message: Optional[discord.Message] = None,
                          raw_reaction: Optional[discord.RawReactionActionEvent] = None) -> None:
    await command.call(client, players_resource, events_resource, guilds_resource, message, raw_reaction, cmd_args)


commands_path = str(Path(__file__).parent)
for module in find_modules(commands_path):
    if 'HelpCommand' != module:
        module = f'{__package__}.{module}'
        importlib.import_module(module, __package__)

BOT_COMMANDS = _get_bot_commands()
