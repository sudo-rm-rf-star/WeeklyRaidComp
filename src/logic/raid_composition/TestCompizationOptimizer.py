from logic.raid_composition.AQRaidCompositionEvaluator import AQRaidCompositionEvaluator
from logic.raid_composition.BWLRaidCompositionEvaluator import BWLRaidCompositionEvaluator
from persistence.TableFactory import TableFactory
import random
from collections import defaultdict

if __name__ == '__main__':
    players_table = TableFactory().get_players_table()
    players = players_table.list_players(615919624034451470)
    characters = {player.get_selected_char() for player in players}
    subset = random.sample(characters, 40)
    chars_by_class_role = defaultdict(lambda: defaultdict(list))
    for char in subset:
        chars_by_class_role[char.role][char.klass].append(char)

    print(BWLRaidCompositionEvaluator(subset).score())
    for role, chars_by_class in chars_by_class_role.items():
        print(role)
        for klazz, chars in chars_by_class.items():
            print(klazz, [char.name for char in chars])


