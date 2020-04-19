from collections import defaultdict

from src.common.Constants import pref_per_role, min_per_class_role, max_per_class_role, VERBOSE
from src.common.Utils import parse_name


class Roster:
    def __init__(self, signees, accepted, bench, absence, missing_roles):
        self.signees = [parse_name(signee) for signee in signees]
        self.accepted = accepted
        self.bench = bench
        self.absence = absence
        self.missing_roles = missing_roles

    def accept_player(self, player):
        success = True
        if player not in self.signees:
            success = False
            message = f"{player} did not accepted the raid event. I cannot add him to the roster. " \
                      f"Add {player} to the raid composition as follows: !addUser [eventID] [ClassRole] {player}. " \
                      f"Contact Dok for further information."
        else:
            if player in self.accepted:
                success = False
                message = f"Player {player} is already accepted"
            elif player in self.bench:
                self.bench.remove(player)
                message = f"Moved {player} from bench to accepted"
            elif player in self.absence:
                self.absence.remove(player)
                message = f"Moved {player} from Accepted to Absence"
            else:
                message = f"Player {player} is now accepted"
        if success:
            self.accepted.append(player)

        return success, message

    def bench_player(self, player):
        success = True

        if player in self.accepted:
            self.accepted.remove(player)
            message = f"Moved {player} from accepted to bench"
        elif player in self.bench:
            success = False
            message = f"Player {player} is already benched"
        elif player in self.absence:
            self.absence.remove(player)
            message = f"Moved {player} from absent to bench"
        else:
            assert player not in self.signees
            message = f"{player} did not sign up. He is now benched."

        if success:
            self.bench.append(player)

        return success, message

    def remove_player(self, player):
        success = True
        if player in self.accepted:
            self.accepted.remove(player)
            message = f"Removed {player} from accepted"
        elif player in self.bench:
            self.bench.remove(player)
            message = f"Removed {player} from benched"
        elif player in self.absence:
            message = f"Removed {player} from absence"
            self.absence.remove(player)
        else:
            success = False
            message = f"Could not find {player}"

        return success, message

    @staticmethod
    def compose(raid, signees):
        missing_roles = {}

        def eligible():
            return signees[(signees['whitelisted'] == 1) & (signees['signup_choice'] == 'Accepted')]

        for role, signees_for_role in eligible().groupby('role'):
            for clazz, signees_for_class in signees_for_role.groupby("class"):
                for i, (j, signee) in enumerate(
                        signees_for_class.sort_values('standby_count', ascending=False).iterrows()):
                    score = _calculate_importance(i, min_per_class_role[raid.name][role][clazz],
                                                  max_per_class_role[raid.name][role][clazz])
                    signees.at[j, "score"] = score

        for role, signees_for_role in eligible().groupby('role'):
            lowest_standby_loc = signees_for_role.sort_values('standby_count', ascending=True).head(n=1).index[0]
            signees.at[lowest_standby_loc, 'score'] = -1
            if VERBOSE:
                print(signees_for_role.sort_values('standby_count', ascending=True).head(n=3))

        for role, signees_for_role in eligible().groupby('role'):
            pref_count = pref_per_role[raid.name][role]
            accepted_for_role = signees_for_role.sort_values('score', ascending=False).iloc[:pref_count]
            accepted_count = accepted_for_role.shape[0]
            if accepted_count < pref_count:
                missing_roles[role] = pref_count - accepted_count
            for j, accepted_signee in accepted_for_role.iterrows():
                signees.at[j, "roster_status"] = 'Accepted'

        chars_per_status = _chars_per_status(signees)
        accepted = chars_per_status['Accepted']
        bench = chars_per_status['Bench']
        absence = chars_per_status['Absence']
        return Roster(signees=raid.signees(),
                      accepted=accepted,
                      bench=bench,
                      absence=absence,
                      missing_roles=missing_roles)


def _calculate_importance(cur, mini, maxi):
    maxi = max(maxi, cur)
    mini = min(mini - 1, cur)
    cur = max(mini, cur)
    return 1 - (cur - mini) / (maxi - mini)


def _chars_per_status(signees):
    records = signees.sort_values(by='class').to_dict(orient='records')
    status_to_char = defaultdict(list)
    for record in records:
        status_to_char[record['roster_status']].append(record['name'])
    return status_to_char


