from pandas import DataFrame
from src.logic.Constant import pref_per_role, min_per_class_role, max_per_class_role, VERBOSE
from logging import getLogger


class Roster:
    def __init__(self, signees):
        self.signees = signees

    @staticmethod
    def compose(raid):
        signees = DataFrame(raid.signees)
        signees.loc[signees['signup_status'] == 'Absence', 'roster_status'] = 'Absence'
        signees.loc[signees['signup_status'] != 'Absence', 'roster_status'] = 'Bench'

        def eligible():
            return signees[(signees['is_kruisvaarder'] == 1) & (signees['signup_status'] == 'Accepted')]

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
                getLogger().warning(f'Only found {accepted_count}/{pref_count} for {role}')
            for j, accepted_signee in accepted_for_role.iterrows():
                signees.at[j, "roster_status"] = 'Accepted'

        return Roster(signees)


def _calculate_importance(cur, mini, maxi):
    maxi = max(maxi, cur)
    mini = min(mini - 1, cur)
    cur = max(mini, cur)
    return 1 - (cur - mini) / (maxi - mini)
