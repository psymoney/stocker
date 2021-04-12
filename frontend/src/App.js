import { HashRouter, Route } from 'react-router-dom';
import Navigation from './components/navigation';
import SignIn from './pages/signin';

function App(props) {
  return (
    <HashRouter>
      <Navigation />
      <Route path="/signin" component={SignIn} />
    </HashRouter>
  );
}

export default App;
