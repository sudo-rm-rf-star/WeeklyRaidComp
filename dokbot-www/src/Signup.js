import { useDrag } from 'react-dnd';

import dragTypes from './DragTypes.js';

export default function Signup({ data }) {
  const [, dragRef] = useDrag(
    () => ({
      type: dragTypes.SIGNUP,
      item: { signup: data },
    }),
    []
  );
  return (<div className="signup" ref={dragRef}>
    {data.name}
  </div>);
};