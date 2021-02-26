from .RaidEventHandler import RaidEventHandler
from .RaidEventCreated import RaidEventCreated
from dokbot.entities.RaidMessage import RaidMessage
from dokbot.entities.RaidNotification import RaidNotification
from dokbot.entities.discord.Member import discord.Member
from dokbot.DiscordGuild import DiscordGuild
from logic.enums.SignupStatus import SignupStatus
from logic.MessageRef import MessageRef
from logic.RaidEvent import RaidEvent
from persistence.MessagesResource import MessagesResource
from persistence.PlayersResource import PlayersResource
from logic.RaidTeam import RaidTeam


class RaidEventCreatedHandler(RaidEventHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def process(self, event: RaidEventCreated):
        raid_event = self.get_raid(guild_id=event.guild_id, team_name=event.team_name, raid_name=event.raid_name,
                                   raid_datetime=event.raid_datetime)
        raid_team = self.get_raidteam(guild_id=event.guild_id, team_name=event.team_name)
        discord_guild = await self.get_discord_guild(event.guild_id, event.team_name)
        await self.send_raid_message(discord_guild, raid_event)
        await self.send_raid_notifications(discord_guild, raid_team, raid_event)
        self.raids_resource.update_raid(raid_event)

    async def send_raid_message(self, discord_guild: DiscordGuild, raid_event: RaidEvent):
        channel = await discord_guild.get_events_channel()

        msg = await RaidMessage.send_message(self.discord_client, discord_guild.guild, raid_event, channel)
        message_ref = MessageRef(message_id=msg.id, guild_id=discord_guild.id, channel_id=channel.id,
                                 raid_name=raid_event.name, raid_datetime=raid_event.datetime,
                                 team_name=raid_event.name)
        MessagesResource().create_channel_message(message_id=msg.id, guild_id=discord_guild.id,
                                                  channel_id=msg.channel.id, raid_name=raid_event.name,
                                                  raid_datetime=raid_event.datetime, team_name=raid_event.name)
        raid_event.message_refs.append(message_ref)

    async def send_raid_notifications(self, discord_guild: DiscordGuild, raid_team: RaidTeam, raid_event: RaidEvent):
        raiders = {raider.discord_id: raider for raider in await discord_guild.get_raiders()}
        messages_resource = MessagesResource()
        players_resource = PlayersResource()

        for discord_id, raider in raiders.items():
            raid_notification = RaidNotification(client=self.discord_client, guild=discord_guild.guild,
                                                 raid_event=raid_event, raidteam=raid_team)
            msg = await raid_notification.send_to(raider)
            if msg:
                messages_resource.create_personal_message(message_id=msg.id, guild_id=discord_guild.id,
                                                          user_id=raider.id, raid_name=raid_event.name,
                                                          raid_datetime=raid_event.datetime,
                                                          team_name=raid_event.team_name)
            player = players_resource.get_player_by_id(discord_id)
            if player:
                raid_event.add_to_signees(player, SignupStatus.UNDECIDED)
