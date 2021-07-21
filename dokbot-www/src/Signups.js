import './Signups.scss';
import { useApi } from './Api';
import Players from './Players';
import usePlayerDrop from "./usePlayerDrop";


export default function Signups() {
  const { unassignedSignups, unassignPlayer } = useApi();
  const [{isOver}, dropRef] = usePlayerDrop(unassignPlayer, [unassignedSignups]); // depend on data updates so we get current spot count

  return (
    <div ref={dropRef} className={`signups${isOver ? ' allow-drop' : ''}`}>
      <header>
        Unassigned signups ( {unassignedSignups.length} )
      </header>
      <div className="signup-roles">
        <Players players={unassignedSignups} />
      </div>
    </div>

  );
}
