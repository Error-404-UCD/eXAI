import React from 'react';
import './App.css';
import Navbar from './JS/Navbar';
import LNavbar from './JS/LNavbar';
import Midbar from './JS/Midbar';
import TopHalf from './JS/TopHalf';
import BottomHalf from './JS/BottomHalf';

function App() {
    return (
        <div className="App">
            <LNavbar />
            <Navbar />
                        <TopHalf />
            <Midbar />
            <BottomHalf />
        </div>
    );
}

export default App;
