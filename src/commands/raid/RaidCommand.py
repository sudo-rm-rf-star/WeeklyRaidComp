from commands.BotCommand import BotCommand
from client.entities.RaidNotification import RaidNotification
from typing import List
from client.entities.GuildMember import GuildMember
from logic.RaidEvent import RaidEvent
from exceptions.InvalidInputException import InvalidInputException
import utils.Logger as Log
from logic.enums.SignupStatus import SignupStatus
from datetime import datetime
from events.raid.RaidEventCreated import RaidEventCreated


class RaidCommand(BotCommand):
    @classmethod
    def name(cls) -> str:
        return "raid"

    async def create_raid(self, raid_name: str, raid_datetime: datetime, is_open: bool):
        guild_id = self.discord_guild.id
        group_id = self.get_raidgroup().id
        if self.events_resource.raid_exists(guild_id, group_id, raid_name, raid_datetime):
            raise InvalidInputException(f'Raid event for {raid_name} on {raid_datetime} already exists.')
        raid_event = RaidEvent(name=raid_name, raid_datetime=raid_datetime, guild_id=guild_id, group_id=group_id,
                               is_open=is_open)
        self.events_resource.create_raid(raid_event)
        self.respond(f'Raid {raid_event} has been successfully created.')
        self.event_queue.send_event(RaidEventCreated(raid_event))
        return raid_event

    async def send_raid_notification(self, raid_event: RaidEvent, raiders: List[GuildMember]) -> None:
        Log.info(f'Sending {len(raiders)} invitations for {raid_event}')
        for raider in raiders:
            if not raid_event.has_user_signed(raider.id) or len(raiders) == 1:
                msg = await RaidNotification(self.client, self.discord_guild, raid_event).send_to(raider)
                if msg:
                    self.messages_resource.create_personal_message(message_id=msg.id, guild_id=self.discord_guild.id,
                                                                   user_id=raider.id, raid_name=raid_event.name,
                                                                   raid_datetime=raid_event.datetime,
                                                                   group_id=raid_event.team_id)

    async def get_unsigned_players(self, raid_event: RaidEvent):
        return [raider for raider in await self.get_raiders() if not raid_event.has_user_signed(raider.id)]

    async def get_tentative_players(self, raid_event: RaidEvent):
        return [raider for raider in await self.get_raiders() if raid_event.has_user_signed_as(raider.id, SignupStatus.TENTATIVE)]
