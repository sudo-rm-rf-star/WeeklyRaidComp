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

  // Hotfix naming of remote images
  let spec = player.spec.toLowerCase() !== 'bear' ?  player.spec.toLowerCase() : 'guardian';

  return (
    <div className={`player ${player.class}`} ref={dragRef}>
      <img src={`https://raw.githubusercontent.com/orourkek/Wow-Icons/master/images/spec/${player.class.toLowerCase()}/${spec}.png`} alt="" />
      <span>{player.name}</span>
      <span className="status-icon">{SignupStatusIcons[player.signupStatus]}</span>
    </div>
  );
}
