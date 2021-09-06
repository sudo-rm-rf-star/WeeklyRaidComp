import {useDrop} from "react-dnd";
import dragTypes from "./DragTypes";

const usePlayerDrop = (onPlayerDrop, deps) => {
  return useDrop(
    () => ({
      accept: dragTypes.PLAYER,
      drop: (item) => {
        if(item) {
            onPlayerDrop(item) ;
        }
      },
      collect: (monitor) => ({
        isOver: monitor.isOver(),
      }),
    }),
    deps
  ); // depend on data updates so we get current spot count
}

export default usePlayerDrop;