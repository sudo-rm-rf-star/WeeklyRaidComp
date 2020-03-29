from RaidReader import get_signees
from RosterWriter import write_roster
from Roster import Roster


if __name__ == '__main__':
    signees = get_signees()
    roster = Roster(signees)
    attendees, standby = roster.compose()
    write_roster(attendees, standby)
