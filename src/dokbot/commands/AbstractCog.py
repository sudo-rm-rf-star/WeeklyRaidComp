import asyncio
from datetime import datetime

from discord.ext.commands import Cog, Context

import utils.Logger as Log
from dokbot.DiscordUtils import get_channel
from dokbot.interactions.RaidTeamSelectionInteraction import RaidTeamSelectionInteraction
from dokbot.utils.CommandUtils import check_authority
from utils.Constants import DATETIMESEC_FORMAT

# Safety measure to avoid infinite loops
MAX_ITERS = 1000000


class AbstractCog(Cog):
    def __init__(self):
        self.raid_team = None

    async def cog_check(self, ctx: Context):
        required_rank = self.raid_team.officer_rank
        check_authority(ctx.author, required_rank)

    async def cog_before_invoke(self, ctx: Context):
        self.log(ctx=ctx)
        if not self.raid_team or self.raid_team.guild_id != ctx.guild.id:
            self.raid_team = await RaidTeamSelectionInteraction.interact(ctx)

    def reply(self, ctx: Context, message: str):
        self.log(ctx=ctx, message=message)
        asyncio.create_task(ctx.reply(content=message))

    def log(self, ctx: Context, message: str = None):
        content = f'{datetime.now().strftime(DATETIMESEC_FORMAT)} - {ctx.author.display_name} - {ctx.command} - {ctx.invoked_with}'
        if message:
            content += f' - {message}'
        if self.raid_team:
            logs_channel = await get_channel(ctx.guild, self.raid_team.logs_channel)
            asyncio.create_task(logs_channel.send(content))
        Log.info(content)
