
class Character:

    def __init__(self, charname, clss, role, is_kruisvaarder, event_status):
        self.charname = charname
        self.clss = clss
        self.role = role
        self.is_kruisvaarder = is_kruisvaarder
        self.event_status = event_status

    def get_score(self):
        return 1

    def __lt__(self, other):
        return self.get_score() < other.get_score()

    def __str__(self):
        return f"{self.charname.capitalize()} {self.role} {self.clss}"
