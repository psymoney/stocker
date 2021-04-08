import logo from './logo.svg';
import './App.css';
import { HashRouter, Route } from 'react-router-dom';
import Navigation from './components/Navigation';
import SignIn from './routes/Signin';
import SignUp from './routes/Signup';

function App(props) {
  console.log(props);
  return (
    <HashRouter>
      <Navigation />
      <Route path="/signin" component={SignIn} />
      <Route path="/signup" component={SignUp} />
    </HashRouter>
  );
}

export default App;
