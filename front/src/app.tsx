import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import GlobalStyles from './globalStyles';
import LoginPage from './pages/LoginPage';
import RegistrationPage from './pages/RegistrationPage';
import MainMenuPage from './pages/MainMenuPage';
import TrainingsPage from './pages/TrainingsPage';
import TrainersPage from './pages/TrainersPage';
import GymsPage from './pages/GymsPage';
import UserTrainsPage from './pages/UserTrainsPage';

const App = () => {
  return (
    <>
      <GlobalStyles />
      <Router>
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route path="/registration" element={<RegistrationPage />} />
          <Route path="/mainmenu" element={<MainMenuPage />} />
          <Route path="/trainings" element={<TrainingsPage />} />
          <Route path="/trainers" element={<TrainersPage />} />
          <Route path="/gyms" element={<GymsPage />} />
          <Route path="/user-trains" element={<UserTrainsPage />} />
        </Routes>
      </Router>
    </>
  );
};

export default App;
