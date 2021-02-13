from exceptions.MissingImplementationException import MissingImplementationException
import discord
from .Event import Event
from dokbot.DiscordGuild import DiscordGuild
from persistence.tables.TableFactory import TableFactory
from utils.Constants import MAINTAINER_ID
import utils.Logger as Log
import traceback


class EventHandler:
    def __init__(self, discord_client: discord.Client):
        self.discord_client = discord_client

    async def process(self, event: Event):
        raise MissingImplementationException(self)

    async def process_failed(self, exception: Exception, event: Event):
        Log.error(f"Failed to process {event} because of {exception}\n{traceback.format_exc()}")
        maintainer = await self.discord_client.fetch_user(MAINTAINER_ID)
        await maintainer.send(f"Failed to process {event}")

    async def get_discord_guild(self, guild_id: int, team_name: str) -> DiscordGuild:
        teams_table = TableFactory().get_raid_teams_table()
        raid_team = teams_table.get_raidteam(guild_id=guild_id, team_name=team_name)
        return await DiscordGuild.create_helper(self.discord_client, raid_team)
