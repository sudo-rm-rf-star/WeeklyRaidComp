"""File full of magic to avoid relying on every single BotCommand"""
from src.commands.BotCommand import BotCommand
from src.exceptions.InvalidCommandException import InvalidCommandException
import importlib
import pkgutil
import os
import discord
from collections import defaultdict

pkg_dir = os.path.dirname(os.path.abspath(__file__))
for (module_loader, name, ispkg) in pkgutil.iter_modules([pkg_dir]):
    importlib.import_module(f'src.commands.{name}', __package__)


def _all_subclasses(cls):
    recursive_subclasses = set()
    if len(cls.__subclasses__()) > 0:
        for subclass in cls.__subclasses__():
            for r_subclass in _all_subclasses(subclass):
                recursive_subclasses.add(r_subclass)
    else:  # Max recursion
        recursive_subclasses.add(cls)

    return recursive_subclasses


def _get_bot_commands():
    bot_commands = defaultdict(dict)
    for command_cls in _all_subclasses(BotCommand):
        command = command_cls()
        bot_commands[command.name][command.subname] = command
    return dict(bot_commands)


BOT_COMMANDS = _get_bot_commands()


async def find_bot_command(message, command_name, subcommand_name):
    command_prefix = command_name[0]
    command_name = command_name[1:]
    if command_prefix == '!' and command_name in BOT_COMMANDS:
        # At this point we can safely delete the message as it is intended for the bot
        try:
            await message.delete()
        except discord.NotFound:  # This happens when multiple versions of the bot are running.
            pass

        if subcommand_name in BOT_COMMANDS[command_name]:
            return BOT_COMMANDS[command_name][subcommand_name]
        else:
            raise InvalidCommandException(f"{command_name} {subcommand_name} is not a valid bot command.")


async def find_and_execute_command(client, message):
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

    if cmd and cmd_args:
        await cmd.call(client, message, cmd_args)
