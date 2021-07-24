import { useApi } from './Api';
import Players from './Players';
import usePlayerDrop from "./usePlayerDrop";


export default function Signups() {
  const { unassignedSignups, unassignPlayer } = useApi();
  const [{isOver}, dropRef] = usePlayerDrop(unassignPlayer, [unassignedSignups]); // depend on data updates so we get current spot count

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
}
