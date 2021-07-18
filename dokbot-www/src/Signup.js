import { useDrag } from 'react-dnd';

import dragTypes from './DragTypes.js';

import './Signup.scss';

const statusIcons = {
  "Accept": "👍",
  "Late": "🕒",
  "Tentative": "🤷",
  "Bench": "🪑",
  "Decline": "👎",
  "Unknown": "❓"
};

export default function Signup({ data }) {
  const [, dragRef] = useDrag(
    () => ({
      type: dragTypes.SIGNUP,
      item: data,
    }),
    []
  );
  return (<div className={`signup ${data.class}`} ref={dragRef}>
    <img src={`/emojis/${data.spec}_${data.class}.png`} alt="" /> {data.name} {statusIcons[data.status]}
  </div>);
};