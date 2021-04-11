import axios from 'axios';
import validator from 'email-validator';

const SIGN_IN_URL = 'user/signin/'


async function requestSignInAPI(email, password) {
  let response
  if (validateEmail(email) === true && validatePassword(password) === true) {
    try {
      response = await axios.post(SIGN_IN_URL, { email: email, password: password }, {
        headers: {
          'Content-Type': 'application/json'
        }
      });
    } catch(error) {
      if (error.response) {
        if (error.response.status === 404) {
          console.error(error.response)
          alert("User not found");
        } else if (error.response.status === 403) {
          alert("Wrong password");
        } else {
          console.error(error.response.data);
          console.error(error.response.status);
          console.error(error.response.headers);
        }
      } else if (error.request) {
        console.error(error.request);
      } else {
        console.error('Error', error.message);
      }
      return null;
    }
    return response.data.accessToken;
  }
  return null;
}

  function validateEmail(email) {
    if (email === '') {
      alert("Enter email");
      return false;
    } else if(!validator.validate(email)) {
      alert("Given email does not follow email format")
      return false
    }
    return true;
  }

  function validatePassword(password) {
    if (password === '') {
      alert("enter password");
      return false;
    }
    return true;
  }

export default requestSignInAPI
