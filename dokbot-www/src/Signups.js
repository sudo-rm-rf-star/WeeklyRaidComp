import Players from './Players';
import usePlayerDrop from "./usePlayerDrop";
import {useStore} from "./RaidEventStoreContext";
import {observer} from 'mobx-react-lite'


const Signups = observer(() => {
  const {raidEvent} = useStore();
  const unassignedSignups = raidEvent.getUnassignedSignups();

  const [{isOver}, dropRef] = usePlayerDrop((player) => raidEvent.unassignPlayer(player), [unassignedSignups]);

  return (
    <div ref={dropRef} className={`signups${isOver ? ' allow-drop' : ''}`}>
      <header>
        Signups ( {unassignedSignups.length} )
      </header>
      <div className="spots">
        <Players players={unassignedSignups} />
      </div>
    </div>

  );
})

export default Signups;