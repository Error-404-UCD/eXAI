import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import LandingPage from './components/LandingPage';
import Main from './components/Main'; 

const App = () => {
  return (
    <Router>
    <Routes>
    <Route path="/" element={<LandingPage />} />
    <Route path="/main" element={<Main />} />
    </Routes>
  </Router>
  );
};

export default App;
