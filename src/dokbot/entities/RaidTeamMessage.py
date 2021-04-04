from .DiscordMessage import DiscordMessage, field
from dokbot.raidteam_actions.ActionsRaidTeam import ActionsRaidTeam
from discord import Embed
from logic.RaidTeam import RaidTeam
from persistence.RaidTeamsResource import RaidTeamsResource
from dokbot.interactions.RaidTeamSelectionInteraction import RaidTeamSelectionInteraction
from dokbot.DokBotContext import DokBotContext
from dokbot.raidteam_actions.ActionsRaidTeam import ActionsRaidTeam

INDENT = 2


class RaidTeamMessage(DiscordMessage):
    def __init__(self, **kwargs):
        super().__init__(**kwargs, reactions=[action.name for action in ActionsRaidTeam])

    @classmethod
    async def make(cls, ctx: DokBotContext, **kwargs):
        if kwargs.get("name"):
            team_name = kwargs["name"]
            raid_team = RaidTeamsResource().get_raidteam(guild_id=ctx.guild.id, team_name=team_name)
            if not raid_team:
                await ctx.reply(f'{team_name} does not exist.')
                return None
        elif kwargs.get("raid_team"):
            raid_team = kwargs["raid_team"]
        else:
            raid_team = await RaidTeamSelectionInteraction.interact(ctx=ctx)
        embed = await cls.get_embed(ctx, raid_team=raid_team)
        return RaidTeamMessage(ctx=ctx, embed=embed)

    @staticmethod
    def title(raid_team: RaidTeam):
        return f"<{raid_team}> What would you like to do?"

    @classmethod
    async def get_embed(cls, ctx: DokBotContext, **kwargs) -> Embed:
        raid_team = kwargs['raid_team']
        embed = {'title': cls.title(raid_team),
                 'description': await _get_description(ctx),
                 'color': 2171428,
                 'type': 'rich'}
        return Embed.from_dict(embed)


async def _get_description(ctx: DokBotContext):
    help_emoji = await ctx.bot.emoji(ActionsRaidTeam.HelpRaidTeam.name)
    return f"Choose one of the buttons. Click {help_emoji} if you don't know where to start."
