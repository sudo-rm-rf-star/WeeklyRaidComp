from client.entities.RaidConsumablesEvaluationMessasge import RaidConsumablesEvaluationMessage
from commands.raid.RaidCommand import RaidCommand
from utils.WarcraftLogs import WarcraftLogs
from utils.DateOptionalTime import DateOptionalTime


class RaidConsumableEvaluate(RaidCommand):
    @classmethod
    def subname(cls) -> str: return "evaluate-consumable"

    @classmethod
    def description(cls) -> str: return "Show consumable usage for a given raid"

    @classmethod
    def argformat(cls) -> str: return "raid_name raid_date raid_time [consumable_name]"

    async def execute(self, raid_name: str, raid_datetime: DateOptionalTime, consumable_name: str, **kwargs):
        self.respond(f"Evaluating the raid, this can take several seconds...")
        destination = self.message.channel
        report = WarcraftLogs(self.guild.wl_guild_id).get_report(raid_name, raid_datetime.date, consumable_name=consumable_name)
        raid_event = self.events_resource.get_raid(self.discord_guild, self.get_raidgroup().group_id, raid_name, raid_datetime)
        if raid_event is None:
            self.respond(f"Could not find an event on {raid_datetime} for {raid_name}")
        elif report is None:
            self.respond(f"Could not find a Warcraft Logs report on {raid_datetime} for {raid_name}")
        else:
            await RaidConsumablesEvaluationMessage(self.client, self.discord_guild, report, raid_event, consumable_name).send_to(destination)

