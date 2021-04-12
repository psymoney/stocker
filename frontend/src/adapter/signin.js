import axios from 'axios';
import validator from 'email-validator';


async function signIn(email, password) {
  let response;
  try {
    response = await axios.post('http://127.0.0.1:8000/user/signin/',
      {
        email: email,
        password: password,
      }, {
        headers: {'Content-Type': 'application/json'},
      });
  } catch (error) {
    if (error.response) {
        return [undefined, error.response.data.message];
      }
    }
    if (error.request) {
      console.error(error.request);
      return [undefined, 'there is no response. try it again.'];
    }
    console.error(error);
    return [undefined, 'unexpected error occurred. try it again.'];
  }
  return [response.data.accessToken, undefined];
}

export default signIn;
