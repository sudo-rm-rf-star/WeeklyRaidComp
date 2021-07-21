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

  const tokenPath = window.location.pathname;
  // const APP_URL = 'http://localhost:5000';
  const APP_URL = '/api'
  const raidUrl = `${APP_URL}/raids${tokenPath}`;

  const getRaidEvent = async () => fetch(raidUrl)
    .then((response) => response.json())
    .then(({data}) => data)

  const {data, isLoading, isError} = useQuery(
    ['raid', tokenPath],
    getRaidEvent,
    // We don't want to override changes of the user to the raid event so we cannot refetch data.
    {staleTime: Infinity});

  const savedRaidEvent = async () => fetch(`${raidUrl}/roster`, {
    method: 'PUT',
    headers: {' Content-Type': 'application/json'},
    body: raidEvent.signups
  })

  const updateRosterMutation = useMutation(savedRaidEvent);

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

  const addRoster = () => {
    setRosters((x) => [...x, {id: rosters.length, name: `Group ${rosters.length + 1}`, spots: []}]);
  };

  const deleteRoster = (roster) => {
    setAssignedSignups((x) => x.except(roster.spots, compareById));
    setRosters((x) => x.except([roster], compareById));
  };
  const changeRosterName = (roster, name) => {
    setRosters((x) => x.map((r) => (r.id === roster.id ? ({...r, name}) : x)));
  };

  const updateSignup = (player, rosterStatus, teamIndex = undefined) => {
    return setRaidEvent((raidEvent) => ({
      ...raidEvent,
      signups: [...raidEvent.signups.filter(({id}) => id !== player.id), {
        ...player,
        rosterStatus,
        teamIndex: teamIndex ?? player.teamIndex
      }]
    }))
  }

  const assignSignupToRoster = (signup, roster) => updateSignup(signup, "Accept", roster.id);

  const benchSignup = (signup) => updateSignup(signup, "Extra");

  const unassignPlayer = (signup) => updateSignup(signup, "Undecided");

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
    unassignPlayer,

    isLoading,
    isError,

    updateRaidEventMutation: updateRosterMutation,
  }}>{children}</Context.Provider>
}