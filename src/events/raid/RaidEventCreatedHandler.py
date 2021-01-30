from events.EventHandler import EventHandler
from .RaidEventCreated import RaidEventCreated
from client.entities.RaidMessage import RaidMessage
from client.entities.RaidNotification import RaidNotification
from client.entities.GuildMember import GuildMember
from logic.enums.SignupStatus import SignupStatus
from logic.MessageRef import MessageRef
from logic.RaidEvent import RaidEvent
from events.DiscordGuild import DiscordGuild
from exceptions.InternalBotException import InternalBotException


class RaidEventCreatedHandler(EventHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def process(self, event: RaidEventCreated):
        raid_event = self.raids_table.get_raid_event(guild_id=event.guild_id, group_id=event.group_id,
                                                     raid_name=event.raid_name, raid_datetime=event.raid_datetime)
        if raid_event is None:
            raise InternalBotException(
                f'Could not find raid event {event.guild_id}/{event.group_id}/{event.raid_name},{event.raid_datetime}')

        discord_guild = await self.get_discord_guild(event.guild_id, event.group_id)

        await self.send_raid_message(discord_guild, raid_event)
        await self.send_raid_notifications(discord_guild, raid_event)
        self.raids_table.update_raid_event(raid_event)

    async def send_raid_message(self, discord_guild: DiscordGuild, raid_event: RaidEvent):
        channel = await discord_guild.get_events_channel()

        msg = await RaidMessage(self.discord_client, discord_guild.discord_guild, raid_event).send_to(channel)
        message_ref = MessageRef(message_id=msg.id, guild_id=discord_guild.id, channel_id=channel.id,
                                 raid_name=raid_event.name, raid_datetime=raid_event.datetime,
                                 group_id=raid_event.team_id)
        self.messages_table.create_channel_message(message_id=msg.id, guild_id=discord_guild.id,
                                                   channel_id=msg.channel.id, raid_name=raid_event.name,
                                                   raid_datetime=raid_event.datetime, group_id=raid_event.team_id)
        raid_event.message_refs.append(message_ref)

    async def send_raid_notifications(self, discord_guild: DiscordGuild, raid_event: RaidEvent):
        raiders = {raider.discord_id: raider for raider in await discord_guild.get_raiders()}
        players = {player.discord_id: player for player in self.players_table.list_players(discord_guild.guild)}

        for discord_id, player in players.items():
            if player.autoinvited:
                member = discord_guild.discord_guild.get_member(player.discord_id)
                if member:
                    raiders[discord_id] = GuildMember(member, discord_guild.id)

        for discord_id, raider in raiders.items():
            raid_notification = RaidNotification(self.discord_client, discord_guild.discord_guild, raid_event)
            msg = await raid_notification.send_to(raider)
            if msg:
                self.messages_table.create_personal_message(message_id=msg.id, guild_id=discord_guild.id,
                                                            user_id=raider.id, raid_name=raid_event.name,
                                                            raid_datetime=raid_event.datetime,
                                                            group_id=raid_event.team_id)
            if discord_id in players:
                raid_event.add_to_signees(players[discord_id], SignupStatus.UNDECIDED)


