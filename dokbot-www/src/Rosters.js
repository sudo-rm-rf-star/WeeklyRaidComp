import './Rosters.scss';
import {useApi} from './Api';
import Roster from "./Roster";

export default function Rosters() {
  const {rosters, addRoster} = useApi();

  return (
    <div className="rosters">
      <div>
        {rosters.orderBy((x) => x.name).map((roster) => (
          <Roster key={roster.name} roster={roster}/>
        ))}
      </div>
      <div className="roster-add">
        <i className="btn fas fa-plus" onClick={addRoster}></i>
      </div>
    </div>
  );
}
