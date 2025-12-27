import React from 'react';

const TestPage: React.FC = () => {
  return (
    <div style={{ padding: '20px', backgroundColor: 'red', color: 'white', minHeight: '100vh' }}>
      <h1>TEST PAGE - If you see this, React is working!</h1>
      <p>This is a basic test page to verify the application is loading.</p>
    </div>
  );
};

export default TestPage;