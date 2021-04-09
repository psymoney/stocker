import React from 'react';
import axios from 'axios';
import { Button } from 'react-bootstrap';

const signInUrl = 'user/signin/'


class SignIn extends React.Component {
  state = {
    accessToken: '',
    email: '',
    password: ''
  }

  redirectToMain = () => {
    console.log(this.props);
    this.props.history.push({pathname: "/main", state: {email: this.state.email, accessToken: this.state.accessToken}});
  }

  appChange = (e) => {
    this.setState({
      [e.target.name]: e.target.value
    });
  }

  appClick = () => {
    this.postAPI();
  }

  appKeyPress = (e) => {
    if (e.key === 'Enter') {
      this.appClick();
    }
  }

  validateEmail = () => {
    if (this.state.email === '') {
      alert("Enter email");
      return false;
    }
    return true;
  }

  validatePassword = () => {
    if (this.state.password === '') {
      alert("enter password");
      return false;
    }
    return true;
  }

  postAPI = async () => {
    let response
    if (this.validateEmail() === true && this.validatePassword() === true) {
      try {
        response = await axios.post(signInUrl, { email: this.state.email, password: this.state.password }, {
          headers: {
            'Content-Type': 'application/json'
          }
        });
      } catch(error) {
        if (error.response) {
          if (error.response.status === 404) {
            alert("User not found");
          } else if (error.response.status === 403) {
            alert("Wrong password");
          } else {
            console.log(error.response.data);
            console.log(error.response.status);
            console.log(error.response.headers);
          }
        } else if (error.request) {
          console.log(error.request);
        } else {
          console.log('Error', error.message);
        }
        return ;
      }
      this.setState({ accessToken: response.data.accessToken });
      this.redirectToMain();
    }
  }

  render() {
    const { appChange, postAPI, appKeyPress } = this;
    return (
      <div>
        <header className="Signin-header">
          <p>Email</p>
          <input type="email" id="inputEmail" className="form-control" placeholder="Enter e-mail" name="email" onChange={appChange} />
          <p>Password</p>
          <input type="password" id="inputPassword" className="form-control" placeholder="Enter password" name="password" onChange={appChange} onKeyPress={appKeyPress}/>
          <br></br>
          <Button type="button" onClick={postAPI} id="submitButton">Sign-In</Button>
        </header>
      </div>
    );
  }
}

export default SignIn