import logo from './logo.svg';
import './App.css';
import { HashRouter, Route } from 'react-router-dom';
import Navigation from './components/Navigation';

function App() {
  return (
    <HashRouter>
      <Navigation />
      <Route />
    </HashRouter>
  );
}

export default App;
