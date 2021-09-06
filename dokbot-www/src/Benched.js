import usePlayerDrop from "./usePlayerDrop";
import Players from "./Players";
import {useStore} from "./RaidEventStoreContext";
import {observer} from 'mobx-react-lite'


const Benched = observer(() => {
  const {raidEvent} = useStore();
  const benched = raidEvent.getBenchedSignups();
  const [{isOver}, dropRef] = usePlayerDrop((player) => raidEvent.benchSignup(player), [benched]);

  return (
    <div ref={dropRef} className={`bench${isOver ? ' allow-drop' : ''}`}>
      <header>
        Benched ( {benched.length} )
      </header>
      <div className="spots">
        {
          (!benched?.length) ?
            (<div key="placeholder" className="roster-spot-placeholder">drag signups here</div>) :
            (<Players players={benched}/>)
        }
      </div>
    </div>
  );
})

export default Benched;