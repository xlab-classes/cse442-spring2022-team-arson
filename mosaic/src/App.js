import React from 'react';
import {BrowserRouter as Router, Routes, Route} from "react-router-dom";
import './App.css';
import LogSign from './Component/logsign.js';
import Login from './Component/login.js';
import Signup from './Component/signup.js';
import Settings from './Component/settings.js';
import SettingsUpdate from './Component/settings_update.js';
import Profile from './Component/profile.js';
import Home from './Component/Home.js';

class App extends React.Component {
  render () {
    return (
      <Router basename={process.env.PUBLIC_URL}>
          <Routes>
              <Route path = "/" element = {<LogSign />} />
              <Route path = "/home" element = {<Home/>} />
              <Route path = "/login" element = {<Login />} />
              <Route path = "/signup" element = {<Signup />} />
              <Route path = "/profile/user/:username" element = {<Profile />} />
              <Route path = "/profile/" element = {<Profile />} />
              <Route path = "/settings" element = {<Settings />} />
              <Route path = "/settings/updated" element = {<SettingsUpdate />} />
          </Routes>
      </Router>
    );
  }
}

export default App;