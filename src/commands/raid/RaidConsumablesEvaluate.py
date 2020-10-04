from client.entities.RaidConsumablesEvaluationMessasge import RaidConsumablesEvaluationMessage
from commands.raid.RaidCommand import RaidCommand
from utils.WarcraftLogs import WarcraftLogs
from utils.DateOptionalTime import DateOptionalTime


class RaidConsumableEvaluate(RaidCommand):
    @classmethod
    def subname(cls) -> str:
        return "evaluate-consumables"

    @classmethod
    def description(cls) -> str:
        return "Show consumable usage for a given raid. This shows amount of pops DURING the " \
               "fights. If a pot was used out of combat, this is not shown. This can be " \
               "useful to track the amount of repots of a protection potion/amount of health " \
               "pots used/... "

    @classmethod
    def argformat(cls) -> str:
        return "raid_name raid_date raid_time"

    @classmethod
    def visible(cls) -> bool: return False

    async def execute(self, raid_name: str, raid_datetime: DateOptionalTime, **kwargs):
        self.respond(f"Evaluating the raid, this can take several seconds...")
        destination = self.message.channel
        raid_event = self.events_resource.get_raid(discord_guild=self.discord_guild, group_id=self.get_group_id(),
                                                   raid_name=raid_name, raid_datetime=raid_datetime)
        report = WarcraftLogs(self.events_resource, self.guild.wl_guild_id).get_report(raid_event)
        if report is None:
            self.respond(f"Could not find a Warcraft Logs report on {raid_datetime} for {raid_name}")
        else:
            await RaidConsumablesEvaluationMessage(self.client, self.discord_guild, report, raid_event).send_to(
                destination)
