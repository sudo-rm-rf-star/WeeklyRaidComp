import { roleOrder } from './constants';
import PlayerList from "./PlayerList";

import './Players.scss';

export default function Players({ players,  horizontal = false }) {
    const playersByRole = players.orderBy(player => player.spec).groupBy(player => player.role)

  return (
      <div className={`players ${horizontal ? "players-horizontal" : "players-vertical"}`}>
          {
              roleOrder.map((role) => (
                  <PlayerList key={role} players={playersByRole[role]}/>
              ))
          }
      </div>
  );
}
