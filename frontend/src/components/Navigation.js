import React from 'react';
import { Button } from 'react-bootstrap';
import { Link } from 'react-router-dom';

class Navigation extends React.Component {
  state = {
    isLoggedIn: false
  };
  render() {
    let signInButton;
    let signUpButton;
    if (this.isLoggedIn) {
      signInButton = <Button>Log out</Button>;
      signUpButton = null;
    } else {
      signInButton = <Button><Link to='/signin'>Sign in</Link></Button>;
      signUpButton = <Button><Link to='/signup'>Sign up</Link></Button>;
    }
    return (
      <div className='navigation'>
        <Button>
          <Link to="/home">Home</Link>
        </Button>
        {signInButton}
        {signUpButton}
      </div>
    );
  }
}

export default Navigation