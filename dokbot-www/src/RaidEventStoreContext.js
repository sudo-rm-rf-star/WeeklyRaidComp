import {createContext, useContext} from "react"
import {RaidEventStore} from "./RaidEventStore";

const Context = createContext(null);

export const useStore = () => useContext(Context);

export const StoreProvider = ({children}) => {
  const tokenPath = window.location.pathname;
  const store = new RaidEventStore(tokenPath);
  return <Context.Provider value={store}>{children}</Context.Provider>
}
