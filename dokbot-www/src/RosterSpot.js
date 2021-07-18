export default function RosterSpot({ data, onDelete }) {
  return <div className="roster-spot">
    <span>{data.signup.name}</span>
    <i className="btn fas fa-trash-alt" onClick={onDelete}></i>
  </div>;
}