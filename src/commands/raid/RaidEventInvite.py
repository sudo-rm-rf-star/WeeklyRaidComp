from commands.raid.RaidCommand import RaidCommand
from utils.DateOptionalTime import DateOptionalTime
from utils.DiscordUtils import get_member, get_member_by_id


class RaidEventInvite(RaidCommand):
    @classmethod
    def subname(cls) -> str: return "invite"

    @classmethod
    def argformat(cls) -> str: return "raid_name discord_name [raid_date][raid_time]"

    @classmethod
    def description(cls) -> str: return "Invites a specific person to the raid. You can use the discord name or " \
                                        "the character name (if the player has already registered)"

    async def execute(self, raid_name: str, discord_name: str, raid_datetime: DateOptionalTime, **kwargs):
        raid_event = self.events_resource.get_raid(discord_guild=self.discord_guild, group_id=self._raidgroup.group_id,
                                                   raid_name=raid_name, raid_datetime=raid_datetime)
        player = self.players_resource.get_player_by_name(discord_name, self.discord_guild.id)
        member = get_member(self.discord_guild, discord_name) if not player else get_member_by_id(self.guild,
                                                                                                  self.player.discord_id)
        if member is None:
            self.respond(f"{discord_name} is not a valid player name. Please use the correct name of the user on discord")
            return
        if raid_event is None:
            self.respond(f'Raid event not found for {raid_name}{f"on {raid_datetime}" if raid_datetime else ""}.')
            return
        await self.send_raid_notification(raid_event=raid_event, raiders=[member])
        self.respond(f'Invited {discord_name} to {raid_event}')
