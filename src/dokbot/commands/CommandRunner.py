import discord
from typing import Optional, List, Dict, Type, Set
from dokbot.commands.BotCommand import BotCommand
from dokbot.commands.character.AddCharacter import AddCharacter
from dokbot.commands.character.ListCharacter import ListCharacter
from dokbot.commands.character.SelectCharacter import SelectCharacter
from dokbot.commands.character.RemoveCharacter import RemoveCharacter
from dokbot.commands.player.AnnounceCommand import AnnounceCommand
from dokbot.commands.player.RegisterPlayerCommand import RegisterPlayerCommand
from dokbot.commands.player.ListAllPlayersCommand import ListAllPlayersCommand
from dokbot.commands.player.ListSelectedPlayersCommand import ListSelectedPlayersCommand
from dokbot.commands.player.AutoInvitePlayer import AutoInvitePlayer
from dokbot.commands.character.SignupCharacterCommand import SignupCharacterCommand
from dokbot.commands.raid.CreateOpenRaid import CreateOpenRaid
from dokbot.commands.raid.CreateClosedRaid import CreateClosedRaid
from dokbot.commands.raid.EditRaidEvent import EditRaidEvent
from dokbot.commands.raid.RemoveRaidEvent import RemoveRaidCommand
from dokbot.commands.raid.RaidEventInvite import RaidEventInvite
from dokbot.commands.raid.RaidEventRemind import RaidEventRemind
from dokbot.commands.raid.OpenRaidEvent import OpenRaidEvent
from dokbot.commands.raid.ShowRaidEvent import ShowRaidEvent
from dokbot.commands.raidteam.SelectRaidGroup import SelectRaidTeam
from dokbot.commands.roster.AcceptPlayerCommand import AcceptPlayerCommand
from dokbot.commands.roster.BenchPlayerCommand import BenchPlayerCommand
from dokbot.commands.roster.DeclinePlayerCommand import DeclinePlayerCommand
from dokbot.commands.roster.CreateRosterCommand import CreateRosterCommand
from dokbot.utils.RegistrationHelper import register
from dokbot.utils.ArgParser import ArgParser
from logic.RaidTeam import RaidTeam
from dokbot.DiscordUtils import get_member_by_id
from collections import defaultdict
from exceptions.InternalBotException import InternalBotException
from exceptions.InvalidInputException import InvalidInputException
from utils.Constants import BOT_NAME
from persistence.MessagesResource import MessagesResource
from persistence.PlayersResource import PlayersResource
from persistence.RaidTeamsResource import RaidTeamsResource

COMMANDS = {AddCharacter, ListCharacter, SelectCharacter, AnnounceCommand, RegisterPlayerCommand,
            SignupCharacterCommand, RemoveRaidCommand, SelectRaidTeam, AcceptPlayerCommand, BenchPlayerCommand,
            DeclinePlayerCommand, CreateRosterCommand, RaidEventInvite, RaidEventRemind, ListAllPlayersCommand,
            CreateClosedRaid, CreateOpenRaid, EditRaidEvent, ListSelectedPlayersCommand, RemoveCharacter,
            OpenRaidEvent, ShowRaidEvent, AutoInvitePlayer}


class CommandRunner:
    def __init__(self, client: discord.Client):
        self.client = client
        self.commands = _to_command_dict(COMMANDS)

    async def run_command_for_message(self, message: discord.Message):
        name, sub_name, argv = None, None, None
        try:
            # Parsing here could be moved to ArgParser
            argv = message.content
            args = tuple(argv.split(' '))
            name, sub_name = tuple(args[:2])
            name = name.strip()[1:]
            argv = ' '.join(args[2:])
        except (IndexError, ValueError):
            pass  # This is not a command intended for our bot.
        if name and sub_name:
            if name not in self.commands:
                return
            if sub_name not in self.commands[name]:
                return
            if message:  # At this point we can safely delete the message as it is intended for the bot
                try:
                    await message.delete()
                except discord.NotFound:  # This happens when multiple versions of the bot are running.
                    pass
                except discord.Forbidden:  # This happens when users are performing actions in DM.
                    pass
            command = await self._create_command(self.commands[name][sub_name], message=message)
            if command:
                if argv == 'help':
                    await message.channel.send(command.get_help())
                else:
                    kwargs = ArgParser(command.argformat()).parse(argv)
                    await command.call(**kwargs)

    async def run_command_for_reaction_event(self, raw_reaction: discord.RawReactionActionEvent,
                                             command_type: Type[BotCommand]):
        command = await self._create_command(command_type, raw_reaction=raw_reaction)
        if command:
            await command.call()

    async def _create_command(self, command_type: Type[BotCommand], message: Optional[discord.Message] = None,
                              raw_reaction: Optional[discord.RawReactionActionEvent] = None) -> Optional[BotCommand]:
        # This code urgently requires refactoring and has grown quite complex over time...

        if raw_reaction:
            user_id = raw_reaction.user_id
            player = PlayersResource().get_player_by_id(user_id)
            message_ref = MessagesResource().get_message(raw_reaction.message_id)
            if message_ref is None:
                return None
            team_name = message_ref.team_name
            guild_id = message_ref.guild_id
            discord_guild = await self.client.fetch_guild(guild_id)
            guild_member = await get_member_by_id(discord_guild, user_id)
            channel = None
        elif message:
            author = message.author
            user_id = author.id
            player = PlayersResource().get_player_by_id(user_id)
            discord_guild = message.guild
            if discord_guild is None:  # This happens when a message is sent in PM.
                if player and player.selected_guild_id:
                    discord_guild = await self.client.fetch_guild(player.selected_guild_id)
                else:
                    raise InvalidInputException("Please execute this command on your dokbot server.")
            team_name = player.selected_team_name
            guild_id = player.selected_guild_id
            guild_member = await get_member_by_id(discord_guild, user_id)
            channel = message.channel
            message_ref = None
        else:
            raise InternalBotException("Either a message or event must be specified")

        if not player:
            await guild_member.send("You need to register a character prior to using DokBot.")
            player, _ = await register(self.client, discord_guild, guild_member)

        # Store that a player was active in this guild
        raidteam: RaidTeam = RaidTeamsResource().get_raidteam(guild_id=guild_id, team_name=team_name)
        return command_type(client=self.client, message=message, message_ref=message_ref, raw_reaction=raw_reaction,
                            member=guild_member, player=player, discord_guild=discord_guild, raidteam=raidteam,
                            channel=channel)


def _to_command_dict(commands: Set[Type[BotCommand]]) -> Dict[str, Dict[str, Type[BotCommand]]]:
    dct = defaultdict(dict)
    for command in commands:
        assert dct.get(command.name(), {}).get(command.sub_name(), None) is None
        dct[command.name()][command.sub_name()] = command
    for name, subcommands in dct.items():
        help_command = generate_help_page_command(name, list(subcommands.values()))
        dct[help_command.name()][help_command.sub_name()] = help_command

    help_command = generate_help_page_command(BOT_NAME.lower(),
                                              [command for _, command_group in dct.items() for _, command in
                                               command_group.items()])
    dct[help_command.name()][help_command.sub_name()] = help_command
    return dict(dct)


def generate_help_page_command(name: str, subcommands: List[Type[BotCommand]]):
    class HelpCommand(BotCommand):
        @classmethod
        def name(cls) -> str: return name

        @classmethod
        def sub_name(cls) -> str: return "help"

        @classmethod
        def req_manager_rank(cls) -> bool: return False

        @classmethod
        def description(
                cls) -> str: return f"Shows all commands for {name} and how to use them. Note that all arguments surround by [ ] are optional."

        async def execute(self, **kwargs) -> None:
            for command in subcommands:
                if command.visible():
                    self.post(command.get_help())

    return HelpCommand
