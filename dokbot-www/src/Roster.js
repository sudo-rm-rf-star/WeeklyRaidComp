import Players from './Players';
import usePlayerDrop from "./usePlayerDrop";
import {useStore} from "./RaidEventStoreContext";
import {observer} from 'mobx-react-lite'


const Roster = observer(({roster}) => {
  const {raidEvent} = useStore();
  const { size } = raidEvent;

  const onPlayerDrop = (player) => raidEvent.assignSignupToRoster(player, roster)
  const [{isOver}, dropRef] = usePlayerDrop(onPlayerDrop, [roster]); // depend on data updates so we get current spot count

  return (
    <div ref={dropRef} className={`roster${isOver ? ' allow-drop' : ''}`}>
      <header>
        <span className="roster-name">{roster.name}</span>
        <span > ( <span className={roster.spots.length > size ? 'length-warning' : ''}>{roster.spots.length}</span> / {size} ) </span>
        <i className="btn fas fa-trash-alt" onClick={() => raidEvent.deleteRoster(roster)}/>
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
})

export default Roster;