import { HashRouter, Route } from 'react-router-dom';
import Navigation from './components/navigation';
import SignIn from './pages/signin';
import SignUp from './pages/signup'

function App(props) {
  return (
    <HashRouter>
      <Navigation />
      <Route path="/signin" component={SignIn} />
      <Route path="/signup" component={SignUp} />
    </HashRouter>
  );
}

export default App;
