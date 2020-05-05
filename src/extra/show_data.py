from src.logic.RaidEvents import RaidEvents
from src.logic.Players import Players


def show_data():
    for event in RaidEvents().all():
        print(event)
        for player_name, signee_choice in event.rosters.signee_choices.items():
            Players().get(player_name, signee_choice)

        for i in range(len(event.rosters.rosters)):
            for player_name, roster_choice in event.rosters.rosters[i].roster_choices.items():
                Players().get(player_name, roster_choice)
    RaidEvents().store()
