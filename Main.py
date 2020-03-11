from InputReader import get_signees
from OutputWriter import write_roster
from Roster import Roster


if __name__ == '__main__':
    signees = get_signees()
    roster = Roster(signees)
    attendees, standby = roster.make_roster()
    write_roster(attendees, standby)
