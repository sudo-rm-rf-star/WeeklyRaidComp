from dokbot.DiscordUtils import *
from logic.RaidTeam import RaidTeam
from logic.RaidEvent import RaidEvent
from exceptions.InternalBotException import InternalBotException
from dokbot.entities.RaidMessage import RaidMessage


class DiscordGuild:
    def __init__(self, client: discord.Client, discord_guild: discord.Guild, raid_team: RaidTeam):
        self.discord_client = client
        self.discord_guild = discord_guild
        self.raid_team = raid_team
        self.id = discord_guild.id

    async def get_events_channel(self) -> discord.TextChannel:
        return await get_channel(self.discord_guild, self.raid_team.events_channel)

    async def get_message(self, message_ref: MessageRef) -> Optional[discord.Message]:
        return await get_message(self.discord_guild, message_ref)

    async def get_raiders(self) -> List[GuildMember]:
        raiders = []
        try:
            async for member in self.discord_guild.fetch_members(limit=None):
                if member and any(role.name == self.raid_team.raider_rank for role in member.roles):
                    raiders.append(GuildMember(member, self.discord_guild.id))
        except discord.Forbidden as e:
            raise InternalBotException(f'There are non-transient problems with Discord permissions...\n{e}')
        return raiders

    async def send_message_to_raiders(self, content: str):
        for raider in await self.get_raiders():
            await raider.send(content)

    async def sync_raid_message(self, raid_event: RaidEvent):
        RaidMessage(self.discord_client, self.discord_guild, raid_event).sync()


async def create_helper(client: discord.Client, raid_team: RaidTeam) -> DiscordGuild:
    discord_guild = await client.fetch_guild(raid_team.guild_id)
    return DiscordGuild(client, discord_guild, raid_team)
