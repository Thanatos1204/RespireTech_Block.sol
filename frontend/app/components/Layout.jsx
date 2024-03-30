// components/Layout.js
import React from 'react';
import Nav from './Navbar';

const Layouts = ({ children }) => {
  return (<>
 
    <div className="relative min-h-screen overflow-hidden">
      <div className="fixed top-0 left-0 w-full h-full bg-cover bg-fixed z-0" style={{ backgroundImage: `url('/levon.png')` }}></div>
      <div className="relative z-10 mx-auto w-4/5">
        {children}
      </div>
    </div>
  </>    
  );
};

export default Layouts;
