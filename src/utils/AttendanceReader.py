from client.PlayersResource import PlayersResource
from client.RaidEventsResource import RaidEventsResource
from client.GuildsResource import GuildsResource
from utils.WarcraftLogs import WarcraftLogs
from utils.DateOptionalTime import DateOptionalTime
from logic.Guild import Guild
from datetime import datetime


def update_raid_presence(guild: Guild, group_id: int, guilds_resource: GuildsResource,
                         events_resource: RaidEventsResource, players_resource: PlayersResource) -> None:
    players = players_resource.list_players(guild)
    raid_events = [raid_event for raid_event in events_resource.get_raids(guild.guild_id, group_id) if
                   raid_event.get_datetime() < DateOptionalTime.now() and raid_event.has_been_scanned]
    attendance = WarcraftLogs(events_resource, guild.wl_guild_id).get_attendance(raid_events)

    for raid_event in raid_events:
        raid_name = raid_event.get_name(abbrev=True)
        raid_datetime = raid_event.get_datetime()
        for player in players:
            was_present = False
            was_standby = False
            for character in player.characters:
                if raid_datetime in attendance.get(character.name, {}).get(raid_name, {}):
                    was_present = True
                    raid_event.presence.add(character.name)
                elif raid_event.has_char_signed(character):
                    was_standby = True
            if was_present:
                player.add_present_date(raid_name, raid_datetime)
            elif was_standby:
                player.add_standby_date(raid_name, raid_datetime)

    for player in players:
        players_resource.update_player(player)

    guild.do_not_scan_before = datetime.now()
    guilds_resource.update_guild(guild)
