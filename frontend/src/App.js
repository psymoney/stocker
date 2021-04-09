import { HashRouter, Route } from 'react-router-dom';
import Navigation from './components/Navigation';
import SignIn from './routes/Signin';

function App(props) {
  console.log(props);
  return (
    <HashRouter>
      <Navigation />
      <Route path="/signin" component={SignIn} />
    </HashRouter>
  );
}

export default App;
