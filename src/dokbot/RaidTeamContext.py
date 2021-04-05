import discord
from logic.Player import Player
from dokbot.DokBot import DokBot
from dokbot.DokBotContext import DokBotContext
from persistence.RaidTeamsResource import RaidTeamsResource
from persistence.PlayersResource import PlayersResource
from typing import List
from logic.Character import Character


class RaidTeamContext(DokBotContext):
    def __init__(self,
                 bot: DokBot,
                 guild: discord.Guild,
                 author: discord.User,
                 channel: discord.TextChannel,
                 team_name: str):
        super().__init__(bot=bot, guild=guild, author=author, channel=channel)
        self.team_name = team_name

    def __getattr__(self, item):
        if item == 'raid_team':
            self.raid_team = RaidTeamsResource().get_raidteam(guild_id=self.guild_id, team_name=self.team_name)
            return self.raid_team

    async def get_events_channel(self) -> discord.TextChannel:
        return await self.bot.fetch_channel(self.raid_team.events_channel)

    async def get_signup_history_channel(self) -> discord.TextChannel:
        return await self.bot.fetch_channel(self.raid_team.signup_history_channel)

    async def get_managers_channel(self) -> discord.TextChannel:
        return await self.bot.fetch_channel(self.raid_team.manager_channel)

    def get_raid_team_players(self) -> List[Player]:
        return list(filter(None, [PlayersResource().get_player_by_id(raider_id) for raider_id in self.raid_team.raider_ids]))

    async def send_to_raiders(self, raiders: List[Character], msg: str):
        for raider in raiders:
            try:
                user = await self.bot.fetch_user(raider.discord_id)
                await user.send(msg)
            except discord.Forbidden:
                await self.reply(f'Could not send a reminder to {raider}')
