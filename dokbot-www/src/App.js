import './App.scss';
import React from 'react';
import RaidEvent from './RaidEvent';
import {StoreProvider} from "./RaidEventStoreContext";

function App() {
  return (
    <div className="App">
      <header>
        <img src="logo.png" alt="logo"/>
        <span>DokBot</span>
      </header>
      <main>
        <StoreProvider>
          <RaidEvent/>
        </StoreProvider>
      </main>
    </div>
  );
}

export default App;
