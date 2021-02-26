from .DiscordMessage import DiscordMessage, field
from .enums.RaidControlAction import RaidControlAction
from discord import Embed
from logic.RaidEvent import RaidEvent
from dokbot.DokBotContext import DokBotContext

INDENT = 2


class RaidControlPanel(DiscordMessage):
    def __init__(self, **kwargs):
        super().__init__(**kwargs, reactions=[action.name for action in RaidTeamControlAction])

    @classmethod
    async def make(cls, ctx: DokBotContext, **kwargs):
        raid = kwargs['raid']
        embed = await cls.get_embed(ctx, raid=raid)
        return RaidControlPanel(ctx=ctx, embed=embed)

    @staticmethod
    def title(raid: RaidEvent):
        return f"Control Panel - {raid}"

    @classmethod
    async def get_embed(cls, ctx: DokBotContext, **kwargs) -> Embed:
        raid = kwargs['raid']
        embed = {'title': cls.title(raid),
                 'description': f"Manage the raid.",
                 'fields': await _get_fields(ctx=ctx),
                 'color': 2171428,
                 'type': 'rich'}
        return Embed.from_dict(embed)


async def _get_fields(ctx: DokBotContext):
    fields = []
    for action in RaidControlAction:
        emoji = await ctx.bot.emoji(action.name)
        entry = "{0} {1}".format(emoji, action.value)
        fields.append(field(entry, inline=False))
    return fields
