from dokbot.RaidContext import RaidContext
from dokbot.raid_actions.PublishRosterChanges import publish_roster_changes
from logic.enums.RosterStatus import RosterStatus
from persistence.PlayersResource import PlayersResource
from persistence.RaidEventsResource import RaidEventsResource
from . import RosterUpdated
from dokbot.entities.RaidMessage import RaidMessage
from ..EventHandler import EventHandler


class RosterUpdatedHandler(EventHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def process(self, event: RosterUpdated):
        raids_resource = RaidEventsResource()
        players_resource = PlayersResource()
        raid_event = raids_resource.get_raid_by_token(event.raid_token)
        roster_changes = event.roster_changes
        if not raid_event or not roster_changes:
            return

        guild = await self.bot.fetch_guild(raid_event.guild_id)
        ctx = RaidContext(bot=self.bot, guild=guild, author=None, channel=None, team_name=raid_event.team_name,
                          raid_name=raid_event.name, raid_datetime=raid_event.datetime)

        updated_characters = []
        for discord_id, (roster_status, team_index) in roster_changes.items():
            player = players_resource.get_player_by_id(discord_id)
            updated_character = ctx.raid_event.add_to_roster(player, RosterStatus[roster_status])
            updated_characters.append(updated_character)

        RaidEventsResource(ctx).update_raid(ctx.raid_event)
        publish_roster_changes(ctx=ctx, characters=updated_characters)
        await RaidMessage.update_messages(ctx=ctx)
