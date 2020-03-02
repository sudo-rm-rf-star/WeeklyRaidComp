
class Attendee:

    def __init__(self, charname, clss, role, is_kruisvaarder, event_status):
        self.charname = charname
        self.clss = clss
        self.role = role
        self.is_kruisvaarder = is_kruisvaarder
        self.event_status = event_status

    def get_score(self):
        return 1 if self.is_kruisvaarder else 0.5

    def compare_score(self, other):
        return self.get_score() > other.get_score
