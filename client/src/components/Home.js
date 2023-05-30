import React from 'react';
import { Link } from 'react-router-dom';

function Home ({ isLoggedIn }) {
  return (
    <div>
      <h1>Neopantry</h1>
      <Link to='/sign-up'>Sign up</Link>
      <Link to='/log-in'>Log in</Link>
    </div>
  );
}

export default Home;
