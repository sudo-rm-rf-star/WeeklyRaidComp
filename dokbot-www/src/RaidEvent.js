import {PacmanLoader} from 'react-spinners';
import Rosters from './Rosters';
import Benched from './Benched';
import Signups from './Signups';
import Declined from "./Declined";
import {useState} from "react";
import {useStore} from "./RaidEventStoreContext";
import {observer} from 'mobx-react-lite'
import Button from './Button'
import {useInterval} from "./utils";


const RaidEvent = observer(() => {
  const store = useStore();
  const [errorMessage, setErrorMessage] = useState();
  const [successMessage, setSuccessMessage] = useState();


  useInterval(async () => {
    await store.loadRaidEvent()
  }, 60000)

  if (store.isLoading) {
    return (<div className="loading"><PacmanLoader color="white"/></div>);
  }

  if (store.isError) {
    return (<div className="internal-error">Something went wrong...</div>);
  }

  if (!store.raidEvent) {
    return (<div className="not-found">Could not find raid...</div>)
  }

  const clearMessages = () => {
    setSuccessMessage("")
    setErrorMessage("")
  }

  const onPublish = () => {
    clearMessages()
    store.saveRaidEvent()
      .then(() => setSuccessMessage("Successfully published your changes!"))
      .catch((err) => {
        setErrorMessage("Failed to publish your changes :-(")
        console.error(err)
      })
  }

  const onDiscard = () => {
    clearMessages();
    store.raidEvent.clearRosterChanges();
  }

  const dt = store.raidEvent.eventAt;
  const date = dt.toISOString().slice(0, 10)
  const time = `${dt.getHours()}:${dt.getMinutes() < 10 ? dt.getMinutes() + '0' : dt.getMinutes()}`

  return (
    <>
      <div className="raid-event">
        <header>
          <div className="raid-event-title">{store.raidEvent.title}</div>
          <div>
            <span className="raid-event-date"> <i className="fas fa-calendar-alt"/> {date} </span>
            <span className="raid-event-time"> <i className="far fa-clock"/> {time} </span>
          </div>
        </header>
        <div className="raid-event-body">
          <div>
            <div className="controls">
              <div className="buttons">
                <Button className="btn publish" onClick={() => onPublish()}
                        disabled={!store.raidEvent.hasRosterChanges()}
                        isLoading={store.isSaving}>Publish</Button>
                <Button className="btn discard" onClick={() => onDiscard()}
                        disabled={!store.raidEvent.hasRosterChanges()}
                        isLoading={store.isLoading}>Discard</Button>
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
})

export default RaidEvent;
