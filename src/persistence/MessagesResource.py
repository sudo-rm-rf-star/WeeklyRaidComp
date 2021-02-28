from persistence.tables.TableFactory import TableFactory
from persistence.tables.MessagesTable import MessagesTable
from logic.MessageRef import MessageRef
from typing import Optional
from datetime import datetime
from logic.RaidEvent import RaidEvent
from dokbot.commands.raidteam.RaidTeamContext import RaidTeamContext
from dokbot.entities.RaidMessage import RaidMessage


class MessagesResource:
    def __init__(self):
        self.messages_table: MessagesTable = TableFactory().get_messages_table()

    def get_message(self, message_id: int) -> Optional[MessageRef]:
        return self.messages_table.get_message(message_id)

    def create_channel_message(self, message_id: int, guild_id: int, channel_id: int, raid_name: str,
                               raid_datetime: datetime, team_name: str):
        return self.messages_table.create_channel_message(message_id=message_id, guild_id=guild_id,
                                                          channel_id=channel_id, raid_name=raid_name,
                                                          raid_datetime=raid_datetime, team_name=team_name)

    def create_personal_message(self, message_id: int, guild_id: int, user_id: int, raid_name: str,
                                raid_datetime: datetime, team_name: str):
        return self.messages_table.create_personal_message(message_id=message_id, guild_id=guild_id, user_id=user_id,
                                                           raid_name=raid_name, raid_datetime=raid_datetime,
                                                           team_name=team_name)

    async def send_raid_message(self, ctx: RaidTeamContext, raid_event: RaidEvent):
        channel = await ctx.guild.get_events_channel()

        msg = await RaidMessage.send_message(ctx.bot, raid_event)
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
