from persistence.TableFactory import TableFactory

if __name__ == '__main__':
    table_factory = TableFactory()
    raid_events_table = table_factory.get_raid_events_table()
    events = raid_events_table.scan()
    for event in events:
        raid_events_table.create_raid_event(event)
        raid_event = raid_events_table.get_raid_event(event.guild_id, event.team_id, event.name, event.get_datetime())