from persistence.tables.TableFactory import TableFactory

if __name__ == '__main__':
    table_factory = TableFactory()
    players_table = table_factory.get_players_table()
    players = players_table.table.scan()
    for player in players['Items']:
        discord_id = player['discord_id']
        player = players_table.get_player_by_id(discord_id)
        print(player.region)
        if player.region == 'Europe':
            player.region = "EU"
            players_table.put_player(player)
