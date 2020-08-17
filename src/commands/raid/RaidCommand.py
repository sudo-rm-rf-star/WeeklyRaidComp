from commands.BotCommand import BotCommand
from logic.RaidEvent import RaidEvent
from client.entities.RaidNotification import RaidNotification
from typing import List
from client.entities.GuildMember import GuildMember
from utils.DateOptionalTime import DateOptionalTime
from exceptions.InvalidArgumentException import InvalidArgumentException


class RaidCommand(BotCommand):
    @classmethod
    def name(cls) -> str:
        return "raid"

    async def send_raid_notification(self, raid_event: RaidEvent, raiders: List[GuildMember]) -> None:
        for raider in raiders:
            if not raid_event.has_user_signed(raider.id):
                msg = await RaidNotification(self.client, self.discord_guild, raid_event).send_to(raider)
                if msg:
                    self.messages_resource.create_personal_message(message_id=msg.id, guild_id=self.discord_guild.id,
                                                                   user_id=raider.id, raid_name=raid_event.name,
                                                                   raid_datetime=raid_event.datetime, group_id=raid_event.group_id)

    async def get_unsigned_players(self, raid_event: RaidEvent):
        return [raider for raider in await self.get_raiders() if not raid_event.has_user_signed(raider.id)]
