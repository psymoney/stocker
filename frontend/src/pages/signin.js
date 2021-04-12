import React from 'react';
import { Button } from 'react-bootstrap';
import validator from 'email-validator';
import signIn from '../adapter/signin';


class SignIn extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      accessToken: '',
      email: '',
      password: '',
    };
  }

  isValidEmail = () => {
    if (this.state.email === '') {
      alert('Enter email');
      return false;
    }
    if (!validator.validate(this.state.email)) {
      alert('Given email does not follow email format');
      return false;
    }
    if (this.state.email.length > 50) {
      alert('Email must be less than 50 characters');
      return false;
    }
    return true;
  };

  isValidPassword = () => {
    if (this.state.password === '') {
      alert('Enter password');
      return false;
    }
    if (this.state.password.length < 8) {
      alert('Wrong password');
      return false;
    }
    return true;
  };

  redirectToMain = () => {
    this.props.history.push({
      pathname: '/main',
      state: {
        email: this.state.email,
        accessToken: this.state.accessToken,
      },
    });
  };

  handleOnChange = (event) => {
    this.setState({
      [event.target.name]: event.target.value,
    });
  };

  handleSubmit = async (event) => {
    event.preventDefault();
    if (!(this.isValidEmail() && this.isValidPassword())) {
      return;
    }
    let [accessToken, errorMessage] = await signIn(this.state.email,
      this.state.password);
    if (errorMessage) {
      alert(errorMessage);
      return;
    }
    this.setState({accessToken});
    this.redirectToMain();
  };

  render() {
    return (
      <div>
        <form onSubmit={this.handleSubmit}>
          <p>Email</p>
          <input type="email" id="inputEmail" className="form-control"
                 placeholder="Enter e-mail" name="email"
                 onChange={this.handleOnChange}/>
          <p>Password</p>
          <input type="password" id="inputPassword" className="form-control"
                 placeholder="Enter password" name="password"
                 onChange={this.handleOnChange}/>
          <br></br>
          <Button type="submit" onClick={this.handleSubmit}
                  id="submitButton">Sign-In</Button>
        </form>
      </div>);
  }
}

export default SignIn;
