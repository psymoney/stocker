import { HashRouter, Route } from 'react-router-dom';
import Navigation from './components/Navigation';
import SignIn from './pages/Signin';

function App(props) {
  return (
    <HashRouter>
      <Navigation />
      <Route path="/signin" component={SignIn} />
    </HashRouter>
  );
}

export default App;
