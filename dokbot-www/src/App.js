import { useState } from 'react';

import Signup from './Signup.js';
import Roster from './Roster.js';

import './App.scss';

function App() {
  const [sequentialId, setSequentialId] = useState(1);
  const generateSequentialId = () => {
    setSequentialId(x => x + 1);
    return sequentialId;
  };

  // TODO: get from db
  const [raidEvents] = useState([
    {
      id: 123,
      title: "Magtheridon's Lair",
      size: 5,
      eventAt: new Date(2021, 7, 8, 19, 30),
      signups: [
        {
          name: "Druantia",
          class: "druid",
          spec: "feral",
          role: "tank"
        },
        {
          name: "Tankié",
          class: "warrior",
          spec: "protection",
          role: "tank"
        },
        {
          name: "Dokk",
          class: "paladin",
          spec: "protection",
          role: "tank"
        },
        {
          name: "Harmi",
          class: "priest",
          spec: "holy",
          role: "healer"
        },
        {
          name: "Shampetter",
          class: "shaman",
          spec: "restoration",
          role: "healer"
        },
        {
          name: "Bledhil",
          class: "rogue",
          spec: "combat",
          role: "melee_dps"
        },
        {
          name: "Nckkh",
          class: "hunter",
          spec: "beast_mastery",
          role: "ranged_dps"
        },
        {
          name: "Soep",
          class: "mage",
          spec: "arcane",
          role: "caster_dps"
        },
        {
          name: "Shikaru",
          class: "priest",
          spec: "shadow",
          role: "caster_dps"
        },
      ]
    }
  ]);

  const roleOrder = ["tank", "healer", "melee_dps", "ranged_dps", "caster_dps"];
  const roleTitles = { "tank": "Tank", "healer": "Healer", "melee_dps": "Melee DPS", "ranged_dps": "Ranged DPS", "caster_dps": "Caster DPS" };

  const [rosters, setRosters] = useState([]);
  const [assignedSignups, setAssignedSignups] = useState([]);

  const model = raidEvents
    .map(x => ({
      ...x,
      signupCount: x.signups.length,
      signups: x.signups.except(assignedSignups).orderBy(x => x.name).groupBy(x => x.role)
    }));

  const addRoster = () => {
    setRosters(x => [...x, { id: generateSequentialId(), name: `Groep ${rosters.length + 1}`, spots: [] }]);
  };

  const deleteRoster = (roster) => {
    setAssignedSignups(x => x.except(roster.spots.map(s => s.signup)));
    setRosters(x => x.except([roster]));
  }

  const changeRosterName = (roster, name) => {
    setRosters(x => x.map(r => r.id === roster.id ? ({ ...r, name }) : x));
  }
  const assignSignupToRoster = (signup, roster) => {
    setAssignedSignups(x => x.concat([signup]));
    setRosters(x => x.map(r => r.id === roster.id ? ({ ...r, spots: [...r.spots, { signup }] }) : r));
  };
  const unassignSignupFromRoster = (signup, roster) => {
    setAssignedSignups(x => x.except([signup]));
    setRosters(x => x.map(r => r.id === roster.id ? ({ ...r, spots: r.spots.filter(s => s.signup !== signup) }) : r));
  }

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
              <div className="raid-event-time"><i className="far fa-clock"></i> {raidEvent.eventAt.toISOString().slice(11, 19)}</div>
            </header>
            <div className="horizontal-break"></div>
            <div className="signups">
              <header>
                Unassigned signups ({raidEvent.signupCount - assignedSignups.length})
              </header>
              <div className="signup-roles">
                {roleOrder
                  .map(role => ({ role, signups: raidEvent.signups[role] }))
                  .filter(x => x.signups)
                  .map(x => {
                    return <div className={x.role} key={x.role}>
                      <div className="signup-role">{roleTitles[x.role]}</div>
                      {x.signups.map(signup => <Signup key={signup.name} data={signup} />)}
                    </div>;
                  })}
              </div>
            </div>
            <div className="horizontal-break"></div>
            <div className="rosters">
              <header>
                Rosters
                <i className="btn fas fa-plus-square" onClick={addRoster}></i>
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
              </div>
            </div>
          </div>)
        }

      </main>
    </div>
  );
}

export default App;