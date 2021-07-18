import { useDrop } from 'react-dnd';

import dragTypes from './DragTypes.js';
import RosterSpot from './RosterSpot.js';

import './Benched.scss';

export default function Benched({ size, data, bench, unbench }) {
  const [{ isOver }, dropRef] = useDrop(
    () => ({
      accept: dragTypes.SIGNUP,
      drop: (item) => {
        if (item) {
          bench(item);
        }
      },
      collect: (monitor) => ({
        isOver: monitor.isOver(),
      }),
    })
    , [data]); // depend on data updates so we get current spot count

  return <div ref={dropRef} className={`bench${isOver ? " allow-drop" : ""}`}>
    <header>
      Benched <span>({data.length})</span>
    </header>
    <div className="bench-spots">
      {data
        .map(spot => <RosterSpot key={spot.name} data={spot} onDelete={() => unbench(spot)} />)
        .concat([<div key="placeholder" className="bench-spot-placeholder">drop signups here</div>])}
    </div>
  </div>;
}