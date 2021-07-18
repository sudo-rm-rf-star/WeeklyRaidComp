import { useDrop } from 'react-dnd';

import dragTypes from './DragTypes.js';
import RosterSpot from './RosterSpot.js';

export default function Roster({ size, data, assignSignupToRoster, unassignSignupFromRoster, onDelete, onRename }) {
  const [{ isOver }, dropRef] = useDrop(
    () => ({
      accept: dragTypes.SIGNUP,
      drop: (item) => {
        if (item && item.signup) {
          if (data.spots.length < size) {
            assignSignupToRoster(item.signup, data);
          }
        }
      },
      collect: (monitor) => ({
        isOver: monitor.isOver(),
      }),
    })
    , [data]); // depend on data updates so we get current spot count

  return <div ref={dropRef} className={`roster${isOver ? " allow-drop" : ""}`}>
    <header>
      <input type="text" placeholder="Groep naam" value={data.name} onChange={(e) => onRename(data, e.target.value)} />
      <span>({data.spots.length}/{size})</span>
      <i className="btn fas fa-trash-alt" onClick={() => onDelete(data)} ></i>
    </header>
    <div className="roster-spots">
      {data.spots
        .map(spot => <RosterSpot key={spot.signup.name} data={spot} onDelete={() => unassignSignupFromRoster(spot.signup, data)} />)
        .concat(data.spots.length < size ? [<div key="placeholder" className="roster-spot-placeholder">drop signups here</div>] : [])}
    </div>
  </div>;
}