from dokbot.commands.raid.RaidContext import RaidContext

async def show_raid(ctx: RaidContext):
    raid_event = await self.get_raid_event(raid_name, raid_datetime)
    await self.send_raid_message(self.channel, raid_event)
    self.events_resource.update_raid(self.discord_guild, raid_event)
