import {useApi} from './Api';
import Players from './Players';
import usePlayerDrop from "./usePlayerDrop";

export default function Roster({roster}) {
  const {assignSignupToRoster, raidEvent: {size}, changeRosterName, deleteRoster} = useApi();
  const onPlayerDrop = (player) => assignSignupToRoster(player, roster)
  const [{isOver}, dropRef] = usePlayerDrop(onPlayerDrop, [roster]); // depend on data updates so we get current spot count

  return (
    <div ref={dropRef} className={`roster${isOver ? ' allow-drop' : ''}`}>
      <header>
        <input
          type="text"
          placeholder="Group name"
          value={roster.name}
          onChange={(e) => changeRosterName(roster, e.target.value)}
        />
        <span > ( <span className={roster.spots.length > size ? 'length-warning' : ''}>{roster.spots.length}</span> / {size} ) </span>
        <i className="btn fas fa-trash-alt" onClick={() => deleteRoster(roster)}/>
      </header>
      <div className="roster-spots">
        {
          !(roster.spots?.length) ?
            (<div key="placeholder" className="roster-spot-placeholder">drag signups here</div>) :
            (<Players players={roster.spots} horizontal={true}/>)
        }
      </div>
    </div>
  );
}
