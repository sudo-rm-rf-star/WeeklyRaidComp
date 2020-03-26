from Constant import expected_raid_size, pref_per_role, min_per_class_role, max_per_class_role, raid


class Roster:
    def __init__(self, signees):
        self.signees = signees
        self.eligible = self.signees[self.signees['kruisvaarder']]

    def make_roster(self):
        for role, signees_for_role in self.eligible.groupby('role'):
            for clazz, signees in signees_for_role.groupby("class"):
                for i, (j, signee) in enumerate(signees.sort_values('standby_count', ascending=False).iterrows()):
                    score = _calculate_importance(i, min_per_class_role[raid][role][clazz],
                                                  max_per_class_role[raid][role][clazz])
                    self.signees.at[j, "score"] = score

        self.eligible = self.signees[self.signees['kruisvaarder']]
        for role, signees_for_role in self.eligible.groupby('role'):
            pref_count = pref_per_role[raid][role]
            accepted_for_role = signees_for_role.sort_values('score', ascending=False).iloc[:pref_count]
            for j, accepted_signee in accepted_for_role.iterrows():
                self.signees.at[j, "raid_status"] = "Accepted"


        accepted = self.signees[self.signees['raid_status'] == 'Accepted']
        standby = self.signees[self.signees['raid_status'] != 'Accepted']
        if accepted.shape[0] != expected_raid_size:
            print('Please manually complete the raid comp!')
            print('====Accepted====')
            print(accepted)
            print('====Standby====')
            print(standby)
        return accepted, standby


def _calculate_importance(cur, mini, maxi):
    maxi = max(maxi, cur)
    mini = min(mini - 1, cur)
    cur = max(mini, cur)
    return 1 - (cur - mini) / (maxi - mini)
