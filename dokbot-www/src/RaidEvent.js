import {PacmanLoader} from 'react-spinners';
import Rosters from './Rosters';
import Benched from './Benched';
import Signups from './Signups';
import {useApi} from './Api';

function RaidEvent() {
  const {raidEvent, isError, isLoading, saveRosterChangesMutation, hasRosterChanges} = useApi();

  if (isLoading) {
    return (<div className="loading"><PacmanLoader color="white"/></div>);
  }

  if (!raidEvent) {
    return (<div className="not-found">Could not find raid...</div>)
  }
  if (!raidEvent || isError) {
    return (<div className="internal-error">Something went wrong...</div>);
  }

  return (
    <>
      <div className="raid-event">
        <header>
          <div className="raid-event-title">{raidEvent.title}</div>
          <div>
            <span className="raid-event-date">
              <i className="fas fa-calendar-alt"/>
              {raidEvent.eventAt.toISOString().slice(0, 10)}
            </span>
            <span className="raid-event-time">
              <i className="far fa-clock"/>
              {raidEvent.eventAt.toTimeString().split(' ')[0]}
            </span>
          </div>
        </header>
        <div className="raid-event-body">
          <Signups/>
          <Rosters/>
          <div>
            <button className="btn publish" onClick={() => saveRosterChangesMutation.mutate()} disabled={!hasRosterChanges}>Publish</button>
            <Benched/>
          </div>
        </div>
      </div>
    </>
  );
}

export default RaidEvent;
