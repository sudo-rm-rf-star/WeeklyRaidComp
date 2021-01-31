from exceptions.MissingImplementationException import MissingImplementationException
import discord
from .Event import Event
from .DiscordGuild import DiscordGuild, create_helper
from persistence.tables.RaidEventsTable import RaidEventsTable
from persistence.tables.GuildsTable import GuildsTable
from persistence.tables.PlayersTable import PlayersTable
from persistence.tables.MessagesTable import MessagesTable
from utils.Constants import MAINTAINER_ID
import utils.Logger as Log
import traceback

class EventHandler:
    def __init__(self, discord_client: discord.Client, raids_table: RaidEventsTable, guilds_table: GuildsTable,
                 players_table: PlayersTable, messages_table: MessagesTable):
        self.discord_client = discord_client
        self.raids_table = raids_table
        self.guilds_table = guilds_table
        self.players_table = players_table
        self.messages_table = messages_table

    async def process(self, event: Event):
        raise MissingImplementationException(self)

    async def process_failed(self, exception: Exception, event: Event):
        Log.error(f"Failed to process {event} because of {exception}\n{traceback.format_exc()}")
        maintainer = await self.discord_client.fetch_user(MAINTAINER_ID)
        await maintainer.send(f"Failed to process {event}")

    async def get_discord_guild(self, guild_id: int, raid_group_id: int = None) -> DiscordGuild:
        guild = self.guilds_table.get_guild(guild_id)
        raid_group = guild.get_raid_group(raid_group_id)
        return await create_helper(self.discord_client, guild, raid_group)
