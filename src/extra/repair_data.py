from src.logic.RaidEvents import RaidEvents

def repair():
    for event in RaidEvents().all():
        for player_name, signee_choice in event.rosters.signee_choices.items():
            if isinstance(signee_choice, tuple):
                event.rosters.signee_choices[player_name] = signee_choice[0]
        for i in range(len(event.rosters.rosters)):
            for player_name, roster_choice in event.rosters.rosters[i].roster_choices.items():
                if isinstance(roster_choice, tuple):
                    event.rosters.rosters[i].roster_choices[player_name] = roster_choice[0]
    RaidEvents().store()






