from .DiscordMessage import DiscordMessage, field
from .enums.RaidTeamControlAction import RaidTeamControlAction
from discord import Embed
from logic.RaidTeam import RaidTeam
from persistence.RaidTeamsResource import RaidTeamsResource
from dokbot.interactions.RaidTeamSelectionInteraction import RaidTeamSelectionInteraction
from dokbot.DokBotContext import DokBotContext

INDENT = 2


class RaidTeamControlPanel(DiscordMessage):
    def __init__(self, **kwargs):
        super().__init__(**kwargs, reactions=[action.name for action in RaidTeamControlAction])

    @classmethod
    async def make(cls, ctx: DokBotContext, **kwargs):
        if kwargs.get("name"):
            team_name = kwargs["name"]
            raid_team = RaidTeamsResource().get_raidteam(guild_id=ctx.guild.id, team_name=team_name)
            if not raid_team:
                await ctx.reply(f'{team_name} does not exist.')
                return None
        else:
            raid_team = await RaidTeamSelectionInteraction.interact(ctx=ctx)
        embed = await cls.get_embed(ctx, raid_team=raid_team)
        return RaidTeamControlPanel(ctx=ctx, embed=embed)

    @staticmethod
    def title(raid_team: RaidTeam):
        return f"<{raid_team}> What would you like to do?"

    @classmethod
    async def get_embed(cls, ctx: DokBotContext, **kwargs) -> Embed:
        raid_team = kwargs['raid_team']
        embed = {'title': cls.title(raid_team),
                 'description': f"Manage and organize raids for your raid team: {raid_team}\n"
                                f"Generate this message again with `>raid {raid_team}`",
                 'fields': await _get_fields(ctx=ctx),
                 'color': 2171428,
                 'type': 'rich'}
        return Embed.from_dict(embed)


async def _get_fields(ctx: DokBotContext):
    fields = []
    for action in RaidTeamControlAction:
        emoji = await ctx.bot.emoji(action.name)
        entry = "{0} {1}".format(emoji, action.value)
        fields.append(field(entry))
    return fields
