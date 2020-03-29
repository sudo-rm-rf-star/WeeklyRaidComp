from pandas import DataFrame
from Constant import pref_per_role, min_per_class_role, max_per_class_role, kruisvaarders_filename
from RosterWriter import write_roster


class Roster:
    def __init__(self, accepted, benched):
        self.accepted = accepted
        self.benched = benched
        self.signees = None

    @staticmethod
    def compose(raid):
        signees = DataFrame(raid.signees)
        signees['accepted'] = False

        def eligible():
            return signees[(signees['is_kruisvaarder']) & (signees['signup_status'] == 'Accepted')]

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

        for role, signees_for_role in eligible().groupby('role'):
            pref_count = pref_per_role[raid.name][role]
            accepted_for_role = signees_for_role.sort_values('score', ascending=False).iloc[:pref_count]
            for j, accepted_signee in accepted_for_role.iterrows():
                signees.at[j, "accepted"] = True

        accepted = signees[signees['accepted']]
        standby = signees[~signees['accepted']]
        print(signees)
        return Roster(accepted, standby)

    def write(self):
        write_roster(self.accepted, self.benched)


def _calculate_importance(cur, mini, maxi):
    maxi = max(maxi, cur)
    mini = min(mini - 1, cur)
    cur = max(mini, cur)
    return 1 - (cur - mini) / (maxi - mini)
