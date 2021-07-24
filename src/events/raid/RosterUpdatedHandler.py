from dokbot.RaidContext import RaidContext
from dokbot.raid_actions.PublishRosterChanges import publish_roster_changes
from persistence.RaidEventsResource import RaidEventsResource
from . import RosterUpdated
from dokbot.entities.RaidMessage import RaidMessage
from ..EventHandler import EventHandler


class RosterUpdatedHandler(EventHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def process(self, event: RosterUpdated):
        raids_resource = RaidEventsResource()
        raid_event = raids_resource.get_raid_by_token(event.raid_token)
        if not raid_event or not event.character_ids:
            return

        guild = await self.bot.fetch_guild(raid_event.guild_id)
        ctx = RaidContext(bot=self.bot, guild=guild, author=None, channel=None, team_name=raid_event.team_name,
                          raid_name=raid_event.name, raid_datetime=raid_event.datetime)
        characters = [raid_event.get_signed_character(discord_id) for discord_id in event.character_ids]
        publish_roster_changes(ctx=ctx, characters=[char for char in characters if char])
        await RaidMessage.update_messages(ctx=ctx)
