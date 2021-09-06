import Player from './Player';

export default function PlayerList({ players }) {
  return players ? (
    <div className="player-list">
      {players.orderBy((player) => [player.class, player.spec, player.name]).map((player) => (
        <Player key={player.id}
          player={player}
        />
      ))}
    </div>
  ) : (<></>);
}
