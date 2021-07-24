import {useApi} from './Api';
import usePlayerDrop from "./usePlayerDrop";
import Players from "./Players";

export default function Declined() {
  const {declined, declineSignup} = useApi();
  const [{isOver}, dropRef] = usePlayerDrop(declineSignup, [declined]); // depend on data updates so we get current spot count

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
}
