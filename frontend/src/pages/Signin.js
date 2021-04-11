import React from 'react';
import { Button } from 'react-bootstrap';
import validator from 'email-validator';
import requestSignInAPI from '../adapter/SigninAPI';


class SignIn extends React.Component {
  constructor() {
    super();
    this.state = {
      accessToken: '',
      email: '',
      password: ''
    }
  }

  redirectToMain = () => {
    this.props.history.push({pathname: "/main", state: {email: this.state.email, accessToken: this.state.accessToken}});
  }

  handleOnChange = (e) => {
    this.setState({
      [e.target.name]: e.target.value
    });
  }

  handleOnKeyPress = (e) => {
    if (e.key === 'Enter') {
      this.authorize();
    }
  }

  authorize = async () => {
    let accessToken = await requestSignInAPI(this.state.email, this.state.password);
    if (accessToken == null) {
      return null;
    }
    this.setState({ accessToken });
    this.redirectToMain();
  }

  render() {
    const { handleOnChange, authorize, handleOnKeyPress } = this;
    return (
      <div>
        <header className="Signin-header">
          <p>Email</p>
          <input type="email" id="inputEmail" className="form-control" placeholder="Enter e-mail" name="email" onChange={handleOnChange} onKeyPress={handleOnKeyPress}/>
          <p>Password</p>
          <input type="password" id="inputPassword" className="form-control" placeholder="Enter password" name="password" onChange={handleOnChange} onKeyPress={handleOnKeyPress}/>
          <br></br>
          <Button type="button" onClick={authorize} id="submitButton">Sign-In</Button>
        </header>
      </div>
    );
  }
}

export default SignIn
