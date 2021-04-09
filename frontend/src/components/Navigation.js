import React from 'react';
import { Link } from 'react-router-dom';

function Navigation() {
  return (
    <div className='navigation'>
      <Link to="/home">Home</Link>
      <Link to="/singin">Sign in</Link>
      <Link to="/signup">Sign up</Link>
    </div>
  );
}

export default Navigation