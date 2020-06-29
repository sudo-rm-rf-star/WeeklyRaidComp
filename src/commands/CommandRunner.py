import discord
from typing import Optional, List, Dict, Type, Set
from commands.BotCommand import BotCommand
from commands.character.AddCharacter import AddCharacter
from commands.character.ListCharacter import ListCharacter
from commands.character.SelectCharacter import SelectCharacter
from commands.guild.CreateGuild import CreateGuild
from commands.player.AnnounceCommand import AnnounceCommand
from commands.player.RegisterPlayerCommand import RegisterPlayerCommand
from commands.player.ListPlayersCommand import ListPlayersCommand
from commands.character.SignupCharacterCommand import SignupCharacterCommand
from commands.raid.CreateOpenRaid import CreateOpenRaid
from commands.raid.CreateClosedRaid import CreateClosedRaid
from commands.raid.RemoveRaidEvent import RemoveRaidCommand
from commands.raid.RaidEventInvite import RaidEventInvite
from commands.raid.RaidEventRemind import RaidEventRemind
from commands.raidgroup.ListRaidGroups import ListRaidGroups
from commands.raidgroup.SelectRaidGroup import SelectRaidGroup
from commands.raidgroup.AddRaidGroup import AddRaidGroup
from commands.roster.AcceptPlayerCommand import AcceptPlayerCommand
from commands.roster.BenchPlayerCommand import BenchPlayerCommand
from commands.roster.DeclinePlayerCommand import DeclinePlayerCommand
from commands.roster.CreateRosterCommand import CreateRosterCommand
from commands.utils.GuildHelper import create_guild
from commands.utils.RegistrationHelper import register
from commands.utils.ArgParser import ArgParser
from client.RaidEventsResource import RaidEventsResource
from client.GuildsResource import GuildsResource
from client.PlayersResource import PlayersResource
from client.MessagesResource import MessagesResource
from logic.RaidGroup import RaidGroup
from utils.DiscordUtils import get_channel, get_member_by_id
from collections import defaultdict
from exceptions.InternalBotException import InternalBotException

COMMANDS = {AddCharacter, ListCharacter, SelectCharacter, CreateGuild, AnnounceCommand, RegisterPlayerCommand, SignupCharacterCommand,
            RemoveRaidCommand, ListRaidGroups, SelectRaidGroup, AddRaidGroup, AcceptPlayerCommand, BenchPlayerCommand, DeclinePlayerCommand,
            CreateRosterCommand, RaidEventInvite, RaidEventRemind, ListPlayersCommand, CreateClosedRaid, CreateOpenRaid}


class CommandRunner:
    def __init__(self, client: discord.Client, players_resource: PlayersResource, events_resource: RaidEventsResource,
                 guilds_resource: GuildsResource, messages_resource: MessagesResource):
        self.client = client
        self.players_resource = players_resource
        self.events_resource = events_resource
        self.guilds_resource = guilds_resource
        self.messages_resource = messages_resource
        self.commands = _to_command_dict(COMMANDS)

    async def run_command_for_message(self, message: discord.Message):
        name, subname, argv = None, None, None
        try:
            # Parsing here could be moved to ArgParser
            argv = message.content
            args = tuple(argv.split(' '))
            name, subname = tuple(args[:2])
            name = name.strip()[1:]
            argv = ' '.join(args[2:])
        except (IndexError, ValueError):
            pass  # This is not a command intended for our bot.
        if name and subname:
            if name not in self.commands:
                return
            if subname not in self.commands[name]:
                return
            if message:  # At this point we can safely delete the message as it is intended for the bot
                try:
                    await message.delete()
                except discord.NotFound:  # This happens when multiple versions of the bot are running.
                    pass
                except discord.Forbidden:  # This happens when users are performing actions in DM.
                    pass
            command = await self._create_command(self.commands[name][subname], message=message)
            if command:
                kwargs = ArgParser(command.argformat()).parse(argv)
                await command.call(**kwargs)

    async def run_command_for_reaction_event(self, raw_reaction: discord.RawReactionActionEvent, command_type: Type[BotCommand]):
        command = await self._create_command(command_type, raw_reaction=raw_reaction)
        if command:
            await command.call()

    async def _create_command(self, command_type: Type[BotCommand], message: Optional[discord.Message] = None,
                              raw_reaction: Optional[discord.RawReactionActionEvent] = None) -> Optional[BotCommand]:
        # This code urgently requires refactoring and has grown quite complex over time...
        if raw_reaction:
            message_ref = self.messages_resource.get_message(raw_reaction.message_id)
            if message_ref is None:
                return None
            guild_id = message_ref.guild_id
            user_id = raw_reaction.user_id
            discord_guild = await self.client.fetch_guild(guild_id)
            guild_member = await get_member_by_id(discord_guild, user_id)
            channel = None
        elif message:
            author = message.author
            user_id = author.id
            discord_guild = message.guild
            if discord_guild is None:  # This happens when a message is sent in PM.
                player = self.players_resource.get_player_by_id(user_id)
                if not player:
                    author.send("Please register first.")
                    return None
                discord_guild = await self.client.fetch_guild(player.guild_id)
            guild_member = await get_member_by_id(discord_guild, user_id)
            channel = message.channel
            message_ref = None
        else:
            raise InternalBotException("Either a message or event must be specified")

        guild = self.guilds_resource.get_guild(discord_guild.id)
        if not guild:
            await guild_member.send("You need to register a guild prior to using DokBot.")
            guild = await create_guild(self.guilds_resource, self.client, discord_guild, guild_member)
        player = self.players_resource.get_player_by_id(user_id)
        if not player:
            await guild_member.send("You need to register a character prior to using DokBot.")
            player = await register(self.client, discord_guild, self.players_resource, guild_member)
        raidgroup: RaidGroup = GuildsResource.get_group(guild, player)
        logs_channel: discord.TextChannel = await get_channel(discord_guild, guild.logs_channel)
        return command_type(client=self.client, players_resource=self.players_resource, events_resource=self.events_resource,
                            guilds_resource=self.guilds_resource, message=message, message_ref=message_ref, raw_reaction=raw_reaction, member=guild_member,
                            player=player, discord_guild=discord_guild, guild=guild, raidgroup=raidgroup, channel=channel, logs_channel=logs_channel,
                            messages_resource=self.messages_resource)


def _to_command_dict(commands: Set[Type[BotCommand]]) -> Dict[str, Dict[str, Type[BotCommand]]]:
    dct = defaultdict(dict)
    for command in commands:
        assert dct.get(command.name(), {}).get(command.subname(), None) is None
        dct[command.name()][command.subname()] = command
    for name, subcommands in dct.items():
        help_command = generate_help_page_command(name, list(subcommands.values()))
        dct[help_command.name()][help_command.subname()] = help_command
    return dict(dct)


def generate_help_page_command(name: str, subcommands: List[Type[BotCommand]]):
    class HelpCommand(BotCommand):
        @classmethod
        def name(cls) -> str: return name

        @classmethod
        def subname(cls) -> str: return "help"

        @classmethod
        def description(cls) -> str: return f"Shows all commands for {name} and how to use them. Note that all arguments surround by [ ] are optional."

        async def execute(self, **kwargs) -> None:
            content = '\n'.join([command.get_help() for command in subcommands])
            self.post(content)

    return HelpCommand
