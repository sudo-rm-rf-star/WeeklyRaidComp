import {PacmanLoader} from 'react-spinners';
import Rosters from './Rosters';
import Benched from './Benched';
import Signups from './Signups';
import {useApi} from './Api';
import Button from "./Button";
import Declined from "./Declined";
import {useState} from "react";

function RaidEvent() {
  const {raidEvent, isError, isLoading, saveRosterChangesMutation, hasRosterChanges, clearRosterChanges} = useApi();
  const [errorMessage, setErrorMessage] = useState();
  const [successMessage, setSuccessMessage] = useState();

  if (isLoading) {
    return (<div className="loading"><PacmanLoader color="white"/></div>);
  }

  if (!raidEvent) {
    return (<div className="not-found">Could not find raid...</div>)
  }
  if (!raidEvent || isError) {
    return (<div className="internal-error">Something went wrong...</div>);
  }

  const clearMessages = () => {
    setSuccessMessage("")
    setErrorMessage("")
  }

  const onPublish = () => {
    clearMessages()
    saveRosterChangesMutation.mutateAsync({})
      .then(() => setSuccessMessage("Successfully published your changes!"))
      .catch(() => setErrorMessage("Failed to publish your changes :-("))
  }

  const onDiscard = () => {
    clearMessages()
    clearRosterChanges()
  }

  const dt = raidEvent.eventAt;
  const date = dt.toISOString().slice(0, 10)
  const time = `${dt.getHours()}:${dt.getMinutes() < 10 ? dt.getMinutes() + '0' : dt.getMinutes()}`

  return (
    <>
      <div className="raid-event">
        <header>
          <div className="raid-event-title">{raidEvent.title}</div>
          <div>
            <span className="raid-event-date"> <i className="fas fa-calendar-alt"/> {date} </span>
            <span className="raid-event-time"> <i className="far fa-clock"/> {time} </span>
          </div>
        </header>
        <div className="raid-event-body">
          <div>
            <div className="controls">
              <div className="buttons">
                <Button className="btn publish" onClick={() => onPublish()} disabled={!hasRosterChanges}
                        isLoading={saveRosterChangesMutation.isLoading}>Publish</Button>
                <Button className="btn discard" onClick={() => onDiscard()} disabled={!hasRosterChanges}
                        isLoading={isLoading}>Discard</Button>
              </div>
              <div>
                {successMessage && (<div className="success"> Successfully published your changes... </div>)}
                {errorMessage && (<div className="error"> Failed to publish your changes... </div>)}
                {!successMessage && !errorMessage && (<br/>)}
              </div>
            </div>
            <Signups/>
          </div>
          <Rosters/>
          <div>
            <Benched/>
            <Declined/>
          </div>
        </div>
      </div>
    </>
  );
}

export default RaidEvent;
