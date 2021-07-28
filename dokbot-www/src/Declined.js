import usePlayerDrop from "./usePlayerDrop";
import Players from "./Players";
import {useStore} from "./RaidEventStoreContext";
import {observer} from 'mobx-react-lite'

const Declined = observer(() => {
  const {raidEvent} = useStore();
  const declined = raidEvent.getDeclinedSignups();

  const [{isOver}, dropRef] = usePlayerDrop((player) => raidEvent.declineSignup(player), [declined]);

  return (
    <div ref={dropRef} className={`declined${isOver ? ' allow-drop' : ''}`}>
      <header>
        Declined ( {declined.length} )
      </header>
      <div className="spots">
        {
          (!declined?.length) ?
            (<div key="placeholder" className="roster-spot-placeholder">drag signups here</div>) :
            (<Players players={declined}/>)
        }
      </div>
    </div>
  );
})

export default Declined;