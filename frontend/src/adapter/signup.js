import axios from 'axios';
import validator from 'email-validator';


async function signUp(email, name, password) {
  let response;
  try {
    response = await axios.post('http://127.0.0.1:8000/user/signup/', {
      email: email,
      userName: name,
      password: password,
    }, {
      headers: {
        'Content-Type': 'application/json',
      },
    });
  } catch (error) {
    if (error.response.status === 409) {
      console.error(error.response);
      return 'Email already exists';
    }
    if (error.response.status === 422) {
      console.error(error.response);
      return 'Invalid input';
    }
    if (error.request) {
      console.error(error.request);
      return 'there is no response. try it again';
    }
    console.error(error);
    return 'Unexpected error occurred. try it again';
  }
  return response;
}

export default signUp;