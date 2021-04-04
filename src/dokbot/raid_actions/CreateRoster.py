from dokbot.RaidContext import RaidContext
from persistence.RaidEventsResource import RaidEventsResource
from .PublishRosterChanges import publish_roster_changes


async def create_roster(ctx: RaidContext):
    updated_characters = ctx.raid_event.compose_roster()
    RaidEventsResource(ctx).update_raid(ctx.raid_event)
    publish_roster_changes(ctx=ctx, characters=updated_characters)
    await ctx.reply(f'Roster for {ctx.raid_event} has been successfully updated. There were {len(updated_characters)} changes')
