import React from 'react';

const RectangleScreen = ({ children }) => {
  return (
    <div className="bg-white bg-opacity-90 rounded-lg p-8 mt-8 shadow-lg" style={{
      background: 'rgba(255, 255, 255, 0.1)', // Semi-transparent background
      backdropFilter: 'blur(20px)', // Blur effect
      boxShadow: '0 8px 32px 0 rgba(0, 0, 0, 0.18)', // Subtle shadow
      borderRadius: '24px', // Rounded corners
      border: '1px solid  rgba(209, 213, 219, 0.18)', 
    }}>
      {children}
    </div>
  );
};

export default RectangleScreen;
