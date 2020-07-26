from commands.raid.RaidCommand import RaidCommand


class ListRaidEvent(RaidCommand):
    @classmethod
    def subname(cls) -> str: return "list"

    @classmethod
    def argformat(cls) -> str: return ""

    @classmethod
    def description(cls) -> str: return "Lists all upcoming raids"

    async def execute(self, **kwargs):
        raid_events = sorted(self.events_resource.get_raids(self.discord_guild.id, self.get_raidgroup().group_id), key=lambda x: x.datetime)
        msg = f"The following raids are upcoming for {self.get_raidgroup()}:\n" + "\n".join(map(str, raid_events))
        self.respond(msg)
