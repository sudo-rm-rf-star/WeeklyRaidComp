from collections import defaultdict


class CharacterSet:
    def __init__(self, characters=None):
        characters = [] if not characters else characters
        self.characters_per_role_and_class = defaultdict(lambda: defaultdict(list))
        for character in characters:
            self.add(character)

    def add(self, character):
        self.characters_per_role_and_class[character.role][character.clss].append(character)

    def role_class_count(self, role, clss):
        return len(self.characters_per_role_and_class[role][clss])

    def role_count(self, role):
        return sum(len(lst) for lst in self.characters_per_role_and_class[role].values())

    def flatten(self):
        characters_list = []
        for characters in self.characters_per_role_and_class.values():
            for character in characters.values():
                characters_list.extend(character)
        return characters_list

    def __str__(self):
        strng = ""
        for role, chars_per_class in self.characters_per_role_and_class.items():
            strng += role + "\n"
            for clss, chars in chars_per_class.items():
                strng += "\n".join(map(str, chars)) + "\n"
        return strng
