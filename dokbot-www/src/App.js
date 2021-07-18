import { useState } from "react";

import Signup from "./Signup";
import Roster from "./Roster";
import Benched from "./Benched";
import Api from "./Api";

import "./App.scss";

function App() {
  const compareById = (l, r) => l.id === r.id;

  const [sequentialId, setSequentialId] = useState(1);
  const generateSequentialId = () => {
    setSequentialId(x => x + 1);
    return sequentialId;
  };

  const [raidEvent] = useState(Api().get_raid());

  const raidNames = { "ml": "Magtheridon's Lair", "gl": "Gruul's Lair", "kara": "Karazhan" };
  const raidSizes = { "ml": 25, "gl": 25, "kara": 10 };
  const specRoles = {
    "Affliction": "caster_dps", "Demonology": "caster_dps", "Destruction": "caster_dps",
    "Discipline": "healer", "Holy": "healer", "Shadow": "caster_dps",
    "Arcane": "caster_dps", "Fire": "caster_dps", "Frost": "caster_dps",
    "Assassination": "melee_dps", "Combat": "melee_dps", "Subtlety": "melee_dps",
    "Balance": "caster_dps", "Feral": "melee_dps", "Bear": "tank", "Restoration": "healer",
    "BeastMastery": "ranged_dps", "Marksmanship": "ranged_dps", "Survival": "ranged_dps",
    "Protection": "tank", "Retribution": "melee_dps",
    "Arms": "melee_dps", "Fury": "melee_dps",
    "Elemental": "caster_dps", "Enhancement": "melee_dps",
  };
  const roleOrder = ["tank", "healer", "melee_dps", "ranged_dps", "caster_dps"];
  const roleTitles = { "tank": "Tank", "healer": "Healer", "melee_dps": "Melee DPS", "ranged_dps": "Ranged DPS", "caster_dps": "Caster DPS" };

  const [rosters, setRosters] = useState([]);
  const [benched, setBenched] = useState([]);
  const [assignedSignups, setAssignedSignups] = useState([]);

  const model = [raidEvent]
    .map(x => ({
      title: raidNames[x.data.name],
      size: raidSizes[x.data.name],
      eventAt: new Date(x.data.timestamp * 1000),
      signupCount: x.data.roster.characters.length,
      signups: x.data.roster.characters
        .map(x => ({
          id: x.discord_id,
          name: x.name,
          role: specRoles[x.spec],
          class: x.class.toLowerCase(),
          spec: x.spec,
          status: x.roster_statuses[x.roster_statuses.length - 1][0]
        }))
        .except(assignedSignups, compareById)
        .orderBy(x => x.name)
        .groupBy(x => x.role)
    }));

  const addRoster = () => {
    setRosters(x => [...x, { id: generateSequentialId(), name: `Groep ${rosters.length + 1}`, spots: [] }]);
  };
  const deleteRoster = (roster) => {
    setAssignedSignups(x => x.except(roster.spots, compareById));
    setRosters(x => x.except([roster], compareById));
  };
  const changeRosterName = (roster, name) => {
    setRosters(x => x.map(r => r.id === roster.id ? ({ ...r, name }) : x));
  };
  const assignSignupToRoster = (signup, roster) => {
    setAssignedSignups(x => x.concat([signup]));
    setRosters(x => x.map(r => r.id === roster.id ? ({ ...r, spots: [...r.spots, signup] }) : r));
  };
  const unassignSignupFromRoster = (signup, roster) => {
    setAssignedSignups(x => x.except([signup], compareById));
    setRosters(x => x.map(r => r.id === roster.id ? ({ ...r, spots: r.spots.except([signup], compareById) }) : r));
  };
  const benchSignup = (signup) => {
    setAssignedSignups(x => x.concat([signup]));
    setBenched(x => x.concat([signup]));
  };
  const unbenchSignup = (signup) => {
    setAssignedSignups(x => x.except([signup], compareById));
    setBenched(x => x.except([signup], compareById));
  };

  return (
    <div className="App">
      <header>
        <img src="logo.png" alt="logo" /> DokBot
      </header>
      <main>
        {
          model.map(raidEvent => <div className="raid-event" key={raidEvent.title}>
            <header>
              <div className="raid-event-title">{raidEvent.title}</div>
              <div className="raid-event-date"><i className="fas fa-calendar-alt"></i> {raidEvent.eventAt.toISOString().slice(0, 10)}</div>
              <div className="raid-event-time"><i className="far fa-clock"></i> {raidEvent.eventAt.toTimeString().split(" ")[0]}</div>
            </header>
            <div className="horizontal-break"></div>
            <div className="raid-event-body">
              <div className="signups">
                <header>
                  Unassigned signups ({raidEvent.signupCount - assignedSignups.length})
                </header>
                <div className="signup-roles">
                  {roleOrder
                    .map(role => ({ role, signups: raidEvent.signups[role] }))
                    .filter(x => x.signups)
                    .map(x => {
                      return <div className={`signup-role ${x.role}`} key={x.role}>
                        <header>{roleTitles[x.role]}</header>
                        <div className="signup-role-items">
                          {x.signups
                            .filter(signup => ["Accept", "Tentative"].indexOf(signup.status) > -1)
                            .map(signup => <Signup key={signup.name} data={signup} />)}
                        </div>
                      </div>;
                    })}
                </div>
              </div>
              <div className="rosters">
                <header>
                  Rosters
                </header>
                <div className="roster-items">
                  {rosters.orderBy(x => x.name).map(roster =>
                    <Roster key={roster.id}
                      size={raidEvent.size}
                      data={roster}
                      onDelete={deleteRoster}
                      onRename={changeRosterName}
                      assignSignupToRoster={assignSignupToRoster}
                      unassignSignupFromRoster={unassignSignupFromRoster}
                    />)}
                  <div className="roster-add">
                    <i className="btn fas fa-plus-square" onClick={addRoster}></i>
                  </div>
                </div>
              </div>
              <Benched
                data={benched}
                bench={benchSignup}
                unbench={unbenchSignup} />
            </div>
          </div>)
        }
      </main>
    </div>
  );
}

export default App;