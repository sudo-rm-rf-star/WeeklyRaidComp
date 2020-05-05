from src.logic.RaidEvents import RaidEvents
from src.logic.enums.RosterStatus2 import RosterStatus
from src.logic.enums.SignupStatus2 import SignupStatus
from src.logic.enums.RosterStatus import RosterStatus as RSOLD


def repair():
    for event in RaidEvents().all():
        for player_name, signee_choice in event.rosters.signee_choices.items():
            print(player_name, signee_choice, signee_choice.value, isinstance(signee_choice, SignupStatus))
            if isinstance(signee_choice.value, tuple):
                print(f'Updated {player_name} with {SignupStatus[signee_choice.name]}')
                # event.rosters.signee_choices[player_name] = SignupStatus[signee_choice.name]
        for i in range(len(event.rosters.rosters)):
            for player_name, roster_choice in event.rosters.rosters[i].roster_choices.items():
                print(player_name, roster_choice, roster_choice.value, isinstance(roster_choice, RSOLD))
                if isinstance(roster_choice.value, tuple):
                    print(f'Updated {player_name} with {RosterStatus[roster_choice.name]}')
                    # event.rosters.rosters[i].roster_choices[player_name] = RosterStatus[roster_choice.name]
    RaidEvents().store()
