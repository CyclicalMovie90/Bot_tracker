import React, { useEffect } from 'react';
import { PassiveTracker } from './PassiveTracker';

const App = () => {
  useEffect(() => {
    const tracker = PassiveTracker();
    tracker.startTracking();
  }, []);

  return (
    <div>
      <h1>Welcome to Passive CAPTCHA</h1>
    </div>
  );
};

export default App;