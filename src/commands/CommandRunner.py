import discord
from typing import Optional, List, Dict, Type
from commands.BotCommand import BotCommand
from commands.character.AddCharacter import AddCharacter
from commands.character.ListCharacter import ListCharacter
from commands.character.SelectCharacter import SelectCharacter
from commands.guild.CreateGuild import CreateGuild
from commands.player.AnnounceCommand import AnnounceCommand
from commands.player.RegisterPlayerCommand import RegisterPlayerCommand
from commands.player.SignupPlayerCommand import SignupPlayerCommand
from commands.raid.CreateRaidCommand import CreateRaidCommand
from commands.raid.RemoveRaidEvent import RemoveRaidCommand
from commands.raidgroup.ListRaidGroups import ListRaidGroups
from commands.raidgroup.SelectRaidGroup import SelectRaidGroup
from commands.raidgroup.AddRaidGroup import AddRaidGroup
from commands.roster.AcceptPlayerCommand import AcceptPlayerCommand
from commands.roster.BenchPlayerCommand import BenchPlayerCommand
from commands.roster.DeclinePlayerCommand import DeclinePlayerCommand
from commands.roster.CreateRosterCommand import CreateRosterCommand
from client.RaidEventsResource import RaidEventsResource
from client.GuildsResource import GuildsResource
from client.PlayersResource import PlayersResource
from client.entities.GuildMember import GuildMember
from logic.Player import Player
from logic.Guild import Guild
from logic.RaidGroup import RaidGroup
from utils.DiscordUtils import get_channel, get_member_by_id
from collections import defaultdict

COMMANDS = [AddCharacter, ListCharacter, SelectCharacter, CreateGuild, AnnounceCommand, RegisterPlayerCommand, SignupPlayerCommand, CreateRaidCommand,
            RemoveRaidCommand, RemoveRaidCommand, ListRaidGroups, SelectRaidGroup, AddRaidGroup, AcceptPlayerCommand, BenchPlayerCommand, DeclinePlayerCommand,
            CreateRosterCommand]


class CommandRunner:
    def __init__(self, client: discord.Client, players_resource: PlayersResource, events_resource: RaidEventsResource,
                 guilds_resource: GuildsResource):
        self.client = client
        self.players_resource = players_resource
        self.events_resource = events_resource
        self.guilds_resource = guilds_resource
        self.commands = _to_command_dict(COMMANDS)

    async def run_command_for_message(self, message: discord.Message):
        try:
            # Parsing here could be moved to ArgParser
            argv = message.content
            args = tuple(argv.split(' '))
            name, subname = tuple(args[:2])
            argv = ' '.join(args[2:])
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
            command = await self._create_command(self.commands[name][subname], message=message, argv=argv)
            await command.call()
        except (IndexError, ValueError):
            pass  # This is not a command intended for our bot.

    async def run_command_for_reaction_event(self, raw_reaction: discord.RawReactionActionEvent, command_type: Type[BotCommand]):
        command = await self._create_command(command_type, raw_reaction=raw_reaction)
        await command.call()

    async def _run_command(self, name: str, subname: str, argv: str, message: Optional[discord.Message] = None,
                           raw_reaction: Optional[discord.RawReactionActionEvent] = None):
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
        command = await self._create_command(self.commands[name][subname], message=message, raw_reaction=raw_reaction, argv=argv)
        await command.call()

    async def _create_command(self, command_type: Type[BotCommand], argv: Optional[str] = None, message: Optional[discord.Message] = None,
                              raw_reaction: Optional[discord.RawReactionActionEvent] = None):
        user_id = raw_reaction.user_id if raw_reaction else message.author.id
        member: GuildMember = get_member_by_id(self.discord_guild, user_id)
        player: Player = self.players_resource.get_player_by_id(member.id)
        self.discord_guild: discord.Guild = await self.client.fetch_guild(player.guild_id) if raw_reaction else message.Guild
        discord_guild: discord.Guild = await self.client.fetch_guild(player.guild_id) if raw_reaction else message.Guild
        guild: Guild = self.guilds_resource.get_guild(member.guild_id)
        raidgroup: RaidGroup = GuildsResource.get_group(guild, player)
        logs_channel: discord.TextChannel = get_channel(discord_guild, guild.logs_channel)
        return command_type(client=self.client, players_resource=self.players_resource, events_resource=self.events_resource,
                            guilds_resource=self.guilds_resource, message=None, raw_reaction=raw_reaction, argv=argv, member=member, player=player,
                            discord_guild=discord_guild, guild=guild, raidgroup=raidgroup, logs_channel=logs_channel)


def _to_command_dict(commands: List[Type[BotCommand]]) -> Dict[str, Dict[str, Type[BotCommand]]]:
    dct = defaultdict(dict)
    for command in commands:
        dct[command.name()][command.subname()] = command
    for name, subcommands in dct.items():
        help_command = generate_help_page_command(name, list(subcommands))
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
            text_channel = self.message.channel
            content = '\n'.join([command.get_help() for command in subcommands])
            await text_channel.send(content)

    return HelpCommand
