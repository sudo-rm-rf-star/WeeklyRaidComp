import './App.scss';
import {QueryClient, QueryClientProvider} from 'react-query';
import React from 'react';
import RaidEvent from './RaidEvent';
import {ApiProvider} from "./Api";


function App() {
  const queryClient = new QueryClient();

  return (
    <div className="App">
      <header>
        <img src="logo.png" alt="logo"/>
        <span>DokBot</span>
      </header>
      <main>
        <QueryClientProvider client={queryClient}>
          <ApiProvider>
            <RaidEvent/>
          </ApiProvider>
        </QueryClientProvider>
      </main>
    </div>
  );
}

export default App;
