from logic.raid_composition.CompositionOptimizer import CompositionOptimizer
from logic.raid_composition.BWLRaidCompositionEvaluator import BWLRaidCompositionEvaluator
from persistence.TableFactory import TableFactory
from logic.Roster import Roster
from logic.enums.RosterStatus import RosterStatus
import random

if __name__ == '__main__':
    players_table = TableFactory().get_players_table()
    players = players_table.list_players(615919624034451470)
    characters = random.sample([player.get_selected_char() for player in players], 42)
    roster = Roster("bwl", characters)
    CompositionOptimizer(roster).make_raid_composition()
    accepted_characters = [character for character in characters if character.roster_status == RosterStatus.ACCEPT]
    declined_characters = [character for character in characters if character.roster_status != RosterStatus.ACCEPT]
    print(BWLRaidCompositionEvaluator(accepted_characters).buff_score())
    print(BWLRaidCompositionEvaluator(accepted_characters).role_score())
    print(BWLRaidCompositionEvaluator(accepted_characters).class_balance_score())
    print(BWLRaidCompositionEvaluator(accepted_characters).raid_specific_score())
    print(BWLRaidCompositionEvaluator(accepted_characters).standby_score())
    print(BWLRaidCompositionEvaluator(accepted_characters).signup_status_score())

    print("ACCEPTED")
    for char in sorted(accepted_characters, key=lambda char: (char.role.name, char.klass.name)):
        print(char)
    print("DECLINED")
    for char in sorted(declined_characters, key=lambda char: (char.role.name, char.klass.name)):
        print(char)

