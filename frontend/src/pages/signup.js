import React from 'react';
import { Button } from 'react-bootstrap';
import validator from 'email-validator';
import signUp from '../adapter/signup';


class SignUp extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      email: '',
      name: '',
      password: '',
      confirmedPassword: '',
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
    if (this.state.password !== this.state.confirmedPassword) {
      alert('Passwords do not match');
      return false;
    }
    if (this.state.password.length < 8) {
      alert('Password must be at least 8 characters');
      return false;
    }
    return true;
  };

  isValidName = () => {
    if (this.state.name === '') {
      alert('Enter name');
      return false;
    }
    return true;
  };

  redirectToMain = () => {
    this.props.history.push('/main');
  };

  handleOnChange = (event) => {
    this.setState({
      [event.target.name]: event.target.value,
    });
  };

  handleSubmit = async (event) => {
    event.preventDefault();
    if (!(this.isValidEmail() && this.isValidPassword() &&
      this.isValidName())) {
      return;
    }
    let errorMessage = await signUp(this.state.email, this.state.name,
      this.state.password);
    if (errorMessage) {
      alert(errorMessage);
      return;
    }
    this.redirectToMain();
  };

  render() {
    return (
      <div className="signup-div">
        <form onSubmit={this.handleSubmit}>
          <p>Email</p>
          <input type="email" id="inputEmail" className="form-control"
                 placeholder="Enter e-mail" name="email"
                 onChange={this.handleOnChange}/>
          <p>Name</p>
          <input type="name" id="inputName" className="form-control"
                 placeholder="Enter name" name="name" onChange={this.handleOnChange}/>
          <p>Password</p>
          <input type="password" id="inputPassword" className="form-control"
                 placeholder="Enter password" name="password"
                 onChange={this.handleOnChange}/>
          <p>Confirm password</p>
          <input type="password" id="inputConfirmedPassword"
                 className="form-control" placeholder="confirm password"
                 name="confirmedPassword" onChange={this.handleOnChange}/>
          <br></br>
          <Button type="submit" onClick={this.handleSubmit}
                  id="submitButton">Sign up</Button>
        </form>
      </div>
    );
  }
}

export default SignUp;
