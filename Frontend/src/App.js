import React from 'react';
import './App.css';
import Navbar from './JS/Navbar';
import LNavbar from './JS/LNavbar';
import Midbar from './JS/Midbar';

function App() {
    return (
        <div className="App">
            <Navbar />
            <LNavbar />
            <Midbar />
        </div>
    );
}

export default App;
