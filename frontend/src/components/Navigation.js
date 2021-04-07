import React from 'react';
import { Button } from 'react-bootstrap';
import { Link } from 'react-router-dom';

class Navigation extends React.Component {
  state = {
    isLoggedIn: false
  };
  render() {
    return (
      <div className='navigation'>
        <Button>
          <Link to="/home">Home</Link>
        </Button>
        <Button color="light">
        {this.isLoggedIn ?
        'Log out' : <Link to='/signin'>Sign in</Link>}
        </Button>
        <Button>
          <Link to="/signup">Sign up</Link>
        </Button>
      </div>
    );
  }
}

export default Navigation