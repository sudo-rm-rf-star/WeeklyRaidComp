from typing import List

from dokbot.RaidContext import RaidContext
from dokbot.RaidTeamContext import RaidTeamContext
from dokbot.entities.RaidMessage import RaidMessage
from dokbot.interactions.OptionInteraction import OptionInteraction
from logic.RaidEvent import RaidEvent
from persistence.RaidEventsResource import RaidEventsResource


async def manage_raid(ctx: RaidTeamContext):
    raids = list(sorted(RaidEventsResource(ctx).list_raids_within_days(guild_id=ctx.guild_id, team_name=ctx.team_name, days=60), key=lambda raid: raid.datetime))
    if len(raids) == 0:
        await ctx.channel.send("There are no raids yet. Please create one first.")
        return
    raid_event = await SelectRaidInteraction.interact(ctx=ctx, raids=raids)
    ctx = RaidContext.from_raid_team_context(ctx, raid_event)
    await RaidMessage.send_for_raid_leaders(ctx)


class SelectRaidInteraction(OptionInteraction):
    def __init__(self, ctx: RaidContext, raids: List[RaidEvent], *args, **kwargs):
        content = "Please choose the raid to manage."
        self.options = [str(raid) for raid in raids]
        self.raids = raids
        super().__init__(ctx=ctx, options=self.options, content=content, *args, **kwargs)

    async def get_response(self) -> RaidEvent:
        result = await super(SelectRaidInteraction, self).get_response()
        i = self.options.index(result)
        return self.raids[i]
