import { useDrag } from 'react-dnd';

import dragTypes from './DragTypes.js';

const SignupStatusIcons = {
  Late: '🕒',
  Tentative: '🤷',
  Bench: '🪑',
  Decline: '👎',
  Unknown: '❓',
};

export default function Player({ player }) {
  const [, dragRef] = useDrag(
    () => ({
      type: dragTypes.PLAYER,
      item: player,
    }),
    [],
  );
  return (
    <div className={`player ${player.class}`} ref={dragRef}>
      <img src={`${process.env.PUBLIC_URL}/emojis/${player.spec}_${player.class}.png`} alt="" />
      <span>{player.name}</span>
      <span className="status-icon">{SignupStatusIcons[player.signupStatus]}</span>
    </div>
  );
}
