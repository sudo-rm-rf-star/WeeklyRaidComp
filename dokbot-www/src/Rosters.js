import './Rosters.scss';
import Roster from "./Roster";
import {useStore} from "./RaidEventStoreContext";
import {observer} from 'mobx-react-lite'

const Rosters = observer(() => {
  const {raidEvent} = useStore();
  const rosters = raidEvent.getRosters();

  return (
    <div className="rosters">
      <div>
        {rosters.orderBy((x) => x.name).map((roster) => (
          <Roster key={roster.name} roster={roster}/>
        ))}
      </div>
    </div>
  );
})

export default Rosters;