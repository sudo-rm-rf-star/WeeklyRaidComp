import {makeAutoObservable, runInAction, autorun} from "mobx"

export class RaidEventStore {
  raidEvent = null
  isError = false;
  isLoading = true
  isSaving = false
  raidUrl = "";

  constructor(tokenPath)  {
    makeAutoObservable(this)
    const appUrl = process.env.NODE_ENV === 'development' ? 'http://localhost:5000' : '/api';
    this.raidUrl = `${appUrl}/raids${tokenPath}`;
    this.loadRaidEvent()
  }

  loadRaidEvent () {
    return fetch(this.raidUrl)
      .then((response) => response.json())
      .then(({data}) => {
        runInAction(() => {
          if(!this.raidEvent) {
            this.raidEvent = new RaidEvent(this, data)
            this.isLoading = false;
          }
        })
      })
      .catch((err) => {
        if(!this.raidEvent) {
          runInAction(() => {
            this.isError = true;
          })
        }
      })
  }

  saveRaidEvent() {
    this.isSaving = true;
    return fetch(`${this.raidUrl}/roster`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(this.raidEvent.rosterChanges)
    }).then(() => {
      runInAction(() => {
        this.raidEvent.rosterChanges = [];
        this.isSaving = false;
      })
    })
  }

}

export class RaidEvent {
  store = null
  json = null

  title = null
  size = null
  eventAt = null
  signups = []

  rosterChanges = null


  constructor(store, json) {
    makeAutoObservable(this)
    this.store = store
    this.json = json
    const savedChanges = localStorage.getItem("rosterChanges");
    this.rosterChanges = savedChanges != null ? JSON.parse(savedChanges)  : {}
    this.updateFromJson()


    autorun(() => {
      if(this.hasRosterChanges()) {
        localStorage.setItem('rosterChanges', JSON.stringify(this.rosterChanges));
      }
    })

    autorun(() => {
      if(this.json != null) {
        runInAction(() => {
          this.updateFromJson()
        })
      }
    })
  }

  getRosters() {
    const rosters = []
    const players = this.signups.filter(({rosterStatus}) => rosterStatus === 'Accept');
    const rosterCount = players.length > 0 ? players.max(({teamIndex}) => teamIndex) + 2 : 1
    for (let i = 0; i < rosterCount; i++) {
      rosters.push({id: i, name: `Roster ${i + 1}`, spots: []});
    }

    players.forEach((player) => {
      rosters[player.teamIndex].spots.push(player)
    })

    return rosters;
  }

  getUnassignedSignups() {
    return this.signups.filter((player) => player.rosterStatus === 'Undecided' && player.signupStatus !== 'Unknown')
  }

  getDeclinedSignups() {
    return this.signups.filter((player) => player.rosterStatus === 'Decline')
  }

  getBenchedSignups() {
    return this.signups.filter((player) => player.rosterStatus === 'Extra')
  }

  deleteRoster(roster) {
    const rosters = this.getRosters()
    this.signups.forEach((player) => {
      const {rosterStatus, teamIndex} = player;
      if(rosterStatus === 'Accept') {
        // Shift everyone one team down.
        if(teamIndex > roster.id)  {
          this.assignSignupToRoster(player, rosters.find(({id}) => id === teamIndex - 1))
        }
        if(teamIndex === roster.id) {
          this.unassignPlayer(player)
        }
      }
    })
  };

  hasRosterChanges() {
    return Object.keys(this.rosterChanges).length > 0;
  }

  updateSignup (player, rosterStatus, teamIndex = undefined) {
    this.signups = [...this.signups.filter(({id}) => id !== player.id), {
      ...player,
      rosterStatus,
      teamIndex: teamIndex ?? player.teamIndex
    }]
    this.rosterChanges[player.id] = [rosterStatus, teamIndex];
  }

  assignSignupToRoster(signup, roster) {
    this.updateSignup(signup, "Accept", roster.id);
  }

  benchSignup(signup) {
    this.updateSignup(signup, "Extra", 0);
  }

  declineSignup(signup) {
    this.updateSignup(signup, "Decline", 0);
  }

  unassignPlayer(signup) {
    this.updateSignup(signup, "Undecided", 0);
  }

  clearRosterChanges() {
    localStorage.removeItem('rosterChanges');
    this.rosterChanges = {};
    this.updateFromJson()
  }

  updateFromJson() {
    this.title = this.json.full_name;
    this.size = this.json.raid_size;
    this.eventAt = new Date(this.json.timestamp * 1000);
    this.signups = this.json.roster.characters
      .map(({discord_id, name, role, class: klass, spec, team_index, roster_status, signup_status}) => {
        const [rosterStatus, teamIndex] = this.rosterChanges[discord_id] ?? [roster_status, team_index]
        return {
          id: discord_id,
          name,
          role,
          class: klass.toLowerCase(),
          spec,
          teamIndex,
          rosterStatus,
          signupStatus: signup_status
        }
      })
  }
}
