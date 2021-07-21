import './Benched.scss';
import {useApi} from './Api';
import usePlayerDrop from "./usePlayerDrop";
import Players from "./Players";

export default function Benched() {
  const {benched, benchSignup} = useApi();
  const [{isOver}, dropRef] = usePlayerDrop(benchSignup, [benched]); // depend on data updates so we get current spot count

  return (
    <div ref={dropRef} className={`bench${isOver ? ' allow-drop' : ''}`}>
      <header>
        Benched ( {benched.length} )
      </header>
      <div className="bench-spots">
        {
          (!benched?.length) ?
            (<div key="placeholder" className="roster-spot-placeholder">drag signups here</div>) :
            (<Players players={benched}/>)
        }
      </div>
    </div>
  );
}
