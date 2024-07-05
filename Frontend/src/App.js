import React from 'react';

import LeftHalf from './components/LeftHalf';
import RightHalf from './components/RightHalf'

function App() {
    return (
      <div className="flex flex-row">
        <LeftHalf />
        <RightHalf />
      </div>
    );
}

export default App;
