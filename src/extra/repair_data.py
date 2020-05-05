from src.logic.RaidEvents import RaidEvents

def repair():
    for event in RaidEvents().all():
        for player_name, signee_choice in event.rosters.signee_choices.items():
            print(player_name, signee_choice.value)
            if isinstance(signee_choice.value, tuple):
                event.rosters.signee_choices[player_name].value = signee_choice.value[0]
        for i in range(len(event.rosters.rosters)):
            for player_name, roster_choice in event.rosters.rosters[i].roster_choices.items():
                print(player_name, roster_choice)
                if isinstance(roster_choice.value, tuple):
                    event.rosters.rosters[i].roster_choices[player_name].value = roster_choice.value[0]
    RaidEvents().store()






