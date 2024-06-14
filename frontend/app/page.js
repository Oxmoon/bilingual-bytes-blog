import './App.css';
import React from 'react';
import { AllPosts } from './components/AllPosts';

function App() {
  //make api call here to fetch sample data.
  return (
    <div className="App">
      <AllPosts />
    </div>
  );
}

export default App;