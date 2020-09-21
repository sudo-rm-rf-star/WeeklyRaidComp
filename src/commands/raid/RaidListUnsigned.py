
from commands.raid.RaidCommand import RaidCommand
from utils.DateOptionalTime import DateOptionalTime


class RaidListUnsigned(RaidCommand):
    @classmethod
    def subname(cls) -> str: return "list-unsigned"

    @classmethod
    def description(cls) -> str: return "List unsigned people for the raid"

    @classmethod
    def argformat(cls) -> str: return "raid_name [raid_date][raid_time]"

    async def execute(self, raid_name: str, raid_datetime: DateOptionalTime, **kwargs):
        raid_event = self.get_raid_event(raid_name, raid_datetime)
        unsigned_discord_ids = {guild_member.id for guild_member in await self.get_unsigned_players(raid_event)}
        unsigned_raiders = [player.get_selected_char().name for player in
                            self.players_resource.list_players(self.guild)
                            if player.discord_id in unsigned_discord_ids]
        self.respond(f'These players have not signed for {raid_event}: {", ".join(map(str, unsigned_raiders))}')
