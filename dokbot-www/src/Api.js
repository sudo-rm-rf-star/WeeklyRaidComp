import {useMutation, useQuery} from 'react-query';
import {createContext, useContext, useEffect, useState} from 'react';
import {bucketedPlayers, mapRaidEventFromApi} from "./ApiUtils";


const Context = createContext(null);

export const useApi = () => {
  return useContext(Context);
};

const compareById = (l, r) => l.id === r.id;


export const ApiProvider = ({children}) => {
  const [raidEvent, setRaidEvent] = useState();
  const [rosters, setRosters] = useState([]);
  const [benched, setBenched] = useState([]);
  const [assignedSignups, setAssignedSignups] = useState([]);
  const [unassignedSignups, setUnassignedSignups] = useState([]);
  const [declined, setDeclined] = useState([]);
  const [rosterChanges, setRosterChanges] = useState([]);

  const tokenPath = window.location.pathname;
  const APP_URL = process.env.NODE_ENV === 'development' ? 'http://localhost:5000' : '/api';
  const raidUrl = `${APP_URL}/raids${tokenPath}`;

  const getRaidEvent = async () => fetch(raidUrl)
    .then((response) => response.json())
    .then(({data}) => data)

  const {data, isLoading, isError, refetch} = useQuery(
    ['raid', tokenPath],
    getRaidEvent,
    // We don't want to override changes of the user to the raid event so we cannot refetch data.
    {staleTime: Infinity});

  const saveRosterChanges = async () => fetch(`${raidUrl}/roster`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(rosterChanges)
  }).then(() => setRosterChanges({}))

  const saveRosterChangesMutation = useMutation(saveRosterChanges);

  useEffect(() => {
    if(data) {
      setRaidEvent(mapRaidEventFromApi(data))
    }
  }, [data])

  useEffect(() => {
    if (raidEvent) {
      const {
        rosters, bench, declined, assignedSignups, unassignedSignups,
      } = bucketedPlayers(raidEvent.signups);
      setRosters(rosters);
      setBenched(bench);
      setAssignedSignups(assignedSignups);
      setDeclined(declined);
      setUnassignedSignups(unassignedSignups)
    }
  }, [raidEvent]);


  const hasRosterChanges = Object.keys(rosterChanges).length > 0

  const addRoster = () => {
    setRosters((x) => [...x, {id: rosters.length, name: `Roster ${rosters.length + 1}`, spots: []}]);
  };

  /** Not supported yet by back-end */
  const deleteRoster = (roster) => {
    roster.spots.forEach((player) => {
      unassignPlayer(player)
    })
    setRosters((x) => x.except([roster], compareById));
  };

  /** Not supported yet by back-end */
  const changeRosterName = (roster, name) => {
    setRosters((x) => x.map((r) => (r.id === roster.id ? ({...r, name}) : x)));
  };

  const updateSignup = (player, rosterStatus, teamIndex = undefined) => {
    const playerId = player.id;
    setRosterChanges((previous) => ({...previous, [playerId]: [rosterStatus, teamIndex]}))
    return setRaidEvent((raidEvent) => ({
      ...raidEvent,
      signups: [...raidEvent.signups.filter(({id}) => id !== playerId), {
        ...player,
        rosterStatus,
        teamIndex: teamIndex ?? player.teamIndex
      }]
    }))
  }

  const assignSignupToRoster = (signup, roster) => updateSignup(signup, "Accept", roster.id);

  const benchSignup = (signup) => updateSignup(signup, "Extra", 0);

  const declineSignup = (signup) => updateSignup(signup, "Decline", 0);

  const unassignPlayer = (signup) => updateSignup(signup, "Undecided", 0);

  const clearRosterChanges = async () => {
    setRaidEvent(mapRaidEventFromApi(data))
    setRosterChanges([])
    await refetch()
  }

  return <Context.Provider value={{
    raidEvent,
    rosters,
    declined,
    benched,
    assignedSignups,
    unassignedSignups,

    addRoster,
    deleteRoster,
    changeRosterName,
    assignSignupToRoster,
    benchSignup,
    declineSignup,
    unassignPlayer,

    isLoading,
    isError,

    hasRosterChanges,
    saveRosterChangesMutation,
    clearRosterChanges
  }}>{children}</Context.Provider>
}