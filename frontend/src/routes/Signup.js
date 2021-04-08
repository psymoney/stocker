import React from 'react';
import axios from 'axios';
import { Button } from 'react-bootstrap';

const signUpUrl = 'user/signup/'


class SignUp extends React.Component {
  state = {
    email: '',
    name: '',
    password: '',
    confirmedPassword: '',
  }

  redirectToMain = () => {
    this.props.history.push("/main");
  }

  appChange = (e) => {
    this.setState({
      [e.target.name]: e.target.value
    });
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

  validateName = () => {
    if (this.state.name === '') {
      alert("Enter name");
      return false;
    }
    return true;
  }

  validatePassword = () => {
    if (this.state.password === '' || this.state.confirmedPassword === '') {
      alert("Enter password");
      return false;
    } else if (this.state.password.length < 8 || this.state.confirmedPassword.length < 8) {
      alert("Password must be at least 8 characters");
      return false;
    } else if (this.state.password !== this.state.confirmedPassword) {
      alert("Passwords didn't match");
      return false;
    }
    return true;
  }

  postAPI = async () => {
    if (this.validateEmail() === true && this.validateName() === true && this.validatePassword() === true) {
      try {
        const response = await axios.post(signUpUrl, { email: this.state.email, userName: this.state.name, password: this.state.password }, {
          headers: {
            'Content-Type': 'application/json'
          }
        });
      } catch(error) {
        if (error.response) {
          if (error.response.status === 409) {
            alert("Email already exists");
          } else if (error.response.status === 422) {
            alert("Invalid input");
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
      this.redirectToMain();
    }
  }

  render() {
    const { appChange, postAPI, appKeyPress } = this;
    return (
      <div>
        <header className="Signup-header">
          <p>Email</p>
          <input type="email" id="inputEmail" className="form-control" placeholder="Enter e-mail" name="email" onChange={appChange} />
          <p>Name</p>
          <input type="name" id="inputName" className="form-control" placeholder="Enter name" name="name" onChange={appChange} />
          <p>Password</p>
          <input type="password" id="inputPassword" className="form-control" placeholder="Enter password" name="password" onChange={appChange}/>
          <p>Confirm password</p>
          <input type="password" id="inputConfirmedPassword" className="form-control" placeholder="Re-enter password" name="confirmedPassword" onChange={appChange} onKeyPress={appKeyPress}/>
          <br></br>
          <Button type="button" onClick={postAPI} id="submitButton">Sign-Up</Button>
        </header>
      </div>
    );
  }
}

export default SignUp