export const mapPlayerFromApi = (player) => ({
  id: player.discord_id,
  name: player.name,
  role: player.role,
  class: player.class.toLowerCase(),
  spec: player.spec,
  teamIndex: player.team_index,
  rosterStatus: player.roster_status,
  signupStatus: player.signup_status
});

export const mapRaidEventFromApi = (data) => (data ? {
  title: data.full_name,
  size: data.raid_size,
  eventAt: new Date(data.timestamp * 1000),
  signups: data.roster.characters.map(mapPlayerFromApi).filter(({signupStatus, rosterStatus}) => signupStatus !== 'Unknown' || rosterStatus !== 'Undecided'),
} : null);


export const bucketedPlayers = (players) => {
  const rosters = [];
  const bench = [];
  const declined = [];
  const assignedSignups = [];
  const unassignedSignups = [];

  const maxTeamIndex = players.max(({teamIndex}) => teamIndex);
  for (let i = 0; i < maxTeamIndex + 1; i++) {
    rosters.push({id: i, name: `Roster ${i + 1}`, spots: []});
  }

  players.forEach((player) => {
    const {rosterStatus, teamIndex} = player;
    switch (rosterStatus) {
      case 'Accept':
        rosters[teamIndex].spots.push(player);
        assignedSignups.push(player);
        break;
      case 'Extra':
        bench.push(player);
        assignedSignups.push(player);
        break;
      case 'Decline':
        declined.push(player);
        break;
      default:
        unassignedSignups.push(player)
        break;
    }
  });

  return {
    rosters, bench, declined, assignedSignups, unassignedSignups
  };
};
