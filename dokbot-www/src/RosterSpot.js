export default function RosterSpot({ data, onDelete }) {
  return <div className={`roster-spot ${data.class}`}>
    <img src={`/emojis/${data.spec}_${data.class}.png`} alt="" />
    <span>{data.name}</span>
    <div></div>
    <i className="btn fas fa-trash-alt" onClick={onDelete}></i>
  </div>;
}