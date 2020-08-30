from commands.BotCommand import BotCommand
from client.entities.RaidNotification import RaidNotification
from typing import List
from client.entities.GuildMember import GuildMember
from client.entities.RaidMessage import RaidMessage
from logic.MessageRef import MessageRef
from logic.RaidEvent import RaidEvent
from utils.DiscordUtils import get_message, get_emoji
from utils.EmojiNames import SIGNUP_STATUS_EMOJI
from utils.DateOptionalTime import DateOptionalTime
from logic.enums.SignupStatus import SignupStatus
from exceptions.InvalidArgumentException import InvalidArgumentException
import discord


class RaidCommand(BotCommand):
    @classmethod
    def name(cls) -> str:
        return "raid"

    async def create_raid(self, raid_name: str, raid_datetime: DateOptionalTime, is_open: bool):
        guild_id = self.discord_guild.id
        group_id = self.get_raidgroup().group_id
        if self.events_resource.raid_exists(guild_id, group_id, raid_name, raid_datetime):
            raise InvalidArgumentException(f'Raid event for {raid_name} on {raid_datetime} already exists.')
        if raid_datetime < DateOptionalTime.now():
            raise InvalidArgumentException('Raid event must be in future')
        raid_event = RaidEvent(name=raid_name, raid_datetime=raid_datetime, guild_id=guild_id, group_id=group_id,
                               is_open=is_open)
        await self.send_raid_message(await self.get_events_channel(), raid_event)
        self.events_resource.create_raid(raid_event)
        raiders = await self.get_raiders()
        await self.send_raid_notification(raid_event=raid_event, raiders=raiders)
        self.respond(f'Raid {raid_event} has been successfully created.')
        return raid_event

    async def send_raid_notification(self, raid_event: RaidEvent, raiders: List[GuildMember]) -> None:
        for raider in raiders:
            if not raid_event.has_user_signed(raider.id) or len(raiders) == 1:
                msg = await RaidNotification(self.client, self.discord_guild, raid_event).send_to(raider)
                if msg:
                    self.messages_resource.create_personal_message(message_id=msg.id, guild_id=self.discord_guild.id,
                                                                   user_id=raider.id, raid_name=raid_event.name,
                                                                   raid_datetime=raid_event.datetime,
                                                                   group_id=raid_event.group_id)

    async def get_unsigned_players(self, raid_event: RaidEvent):
        return [raider for raider in await self.get_raiders() if not raid_event.has_user_signed(raider.id)]

    async def send_raid_message(self, channel: discord.TextChannel, raid_event: RaidEvent):
        msg = await RaidMessage(self.client, self.discord_guild, raid_event).send_to(channel)
        # There's probably some refactoring possible here.
        message_ref = MessageRef(message_id=msg.id, guild_id=self.discord_guild.id, channel_id=channel.id,
                                 raid_name=raid_event.name, raid_datetime=raid_event.datetime,
                                 group_id=raid_event.group_id)
        self.messages_resource.create_channel_message(message_id=msg.id, guild_id=self.discord_guild.id,
                                                      channel_id=msg.channel.id, raid_name=raid_event.name,
                                                      raid_datetime=raid_event.datetime, group_id=raid_event.group_id)
        raid_event.message_refs.append(message_ref)
