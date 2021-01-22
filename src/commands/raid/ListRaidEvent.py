from commands.raid.RaidCommand import RaidCommand


class ListRaidEvent(RaidCommand):
    @classmethod
    def sub_name(cls) -> str: return "list"

    @classmethod
    def argformat(cls) -> str: return ""

    @classmethod
    def description(cls) -> str: return "Lists all the existing raid events"

    async def execute(self, **kwargs):
        raid_events = sorted(self.events_resource.get_raids(self.discord_guild.id, self.get_raidgroup().group_id), key=lambda x: x.datetime)
        msg = f"These are all of the existing raids for {self.get_raidgroup()}:\n" + "\n".join(map(str, raid_events))
        self.respond(msg)
