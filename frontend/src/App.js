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
import HomeRandom from './Component/HomeRandom.js';
import HomeKeyword from './Component/HomeKeyword.js';
import Results from './Component/Results.js';
import View from './Component/View.js';

function App() {
  return (
    <>
      <Router>
          <Routes>
              <Route path = "/" element = {<LogSign />} />
              <Route path = "/home" element = {<Home/>} />
              <Route path = "/home/upload" element = {<Home/>} />
              <Route path = "/home/keyword" element = {<HomeKeyword/>} />
              <Route path = "/home/random" element ={<HomeRandom/>} />
              <Route path = "/login" element = {<Login />} />
              <Route path = "/signup" element = {<Signup />} />
              <Route path = "/profile/" element = {<Profile />} />
              <Route path = "/settings" element = {<Settings />} />
              <Route path = "/settings/updated" element = {<SettingsUpdate />} />
              <Route path = "/results/:privacy" element = {<Results />} />
              <Route path = "/view/id/:id" element = {<View />} />
          </Routes>
      </Router>
    </>
  );
}

export default App;
