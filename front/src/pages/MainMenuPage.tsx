import React from 'react';
import styled from 'styled-components';
import { useNavigate, useLocation } from 'react-router-dom';
import workoutImage from '../assets/workout.jpg'; // Убедитесь, что путь правильный

const MainMenuPage = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { userId } = location.state || {}; // Получаем userId из state

  const handleNavigation = (path: string) => {
    navigate(path, { state: { userId } }); // Передаем userId на другие страницы
  };

  return (
    <PageContainer>
      <Header>
        <Title>FitnessNet</Title>
        <ContactInfo>
          <Email>FitnessNet@fit.com</Email>
          <Phone>+7 (915)-411-21-02</Phone>
        </ContactInfo>
      </Header>
      <Content>
        <MenuContainer>
          <MenuButton onClick={() => handleNavigation('/trainings')}>Тренировки</MenuButton>
          <MenuButton onClick={() => handleNavigation('/trainers')}>Тренеры</MenuButton>
          <MenuButton onClick={() => handleNavigation('/gyms')}>Залы сети</MenuButton>
          <MenuButton onClick={() => handleNavigation('/user-trains')}>Профиль</MenuButton>
          <ExitButton onClick={() => navigate('/login')}>Выход</ExitButton>
        </MenuContainer>
        <RightContainer>
          <WorkoutImage src={workoutImage} alt="Workout" />
        </RightContainer>
      </Content>
    </PageContainer>
  );
};

export default MainMenuPage;

// Styled components
const PageContainer = styled.div`
  display: flex;
  flex-direction: column;
  height: 100vh;
  background-color: #000;
  color: #fff;
`;

const Header = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #ff7b00;
  padding: 0 20px;
  height: 60px;

  @media (max-width: 480px) {
    height: 50px;
    flex-direction: column;
    align-items: flex-start;
    padding: 10px;
  }
`;

const Title = styled.h1`
  font-size: 18px;

  @media (max-width: 480px) {
    font-size: 16px;
  }
`;

const ContactInfo = styled.div`
  text-align: right;

  @media (max-width: 480px) {
    text-align: left;
    margin-top: 5px;
  }
`;

const Email = styled.p`
  margin: 0;
  font-size: 14px;
`;

const Phone = styled.p`
  margin: 0;
  font-size: 14px;
`;

const Content = styled.div`
  display: flex;
  flex: 1;
  justify-content: space-between;
  align-items: center;

  @media (max-width: 480px) {
    flex-direction: column;
    align-items: center;
    padding: 10px;
  }
`;

const MenuContainer = styled.div`
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: flex-start;
  padding-left: 50px;

  @media (max-width: 480px) {
    padding-left: 0;
    align-items: center;
    margin-bottom: 20px;
  }
`;

const MenuButton = styled.button`
  width: 200px;
  padding: 15px;
  margin: 10px 0;
  background-color: #ff7b00;
  color: #fff;
  border: none;
  border-radius: 5px;
  font-size: 18px;
  cursor: pointer;
  transition: background-color 0.3s;

  &:hover {
    background-color: #e67000;
  }

  @media (max-width: 480px) {
    width: 100%;
    font-size: 16px;
    padding: 12px;
  }
`;

const ExitButton = styled(MenuButton)`
  background-color: #555;

  &:hover {
    background-color: #444;
  }

  @media (max-width: 480px) {
    width: 100%;
    font-size: 16px;
    padding: 12px;
  }
`;

const RightContainer = styled.div`
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;

  @media (max-width: 480px) {
    flex: 0;
    margin-top: 20px;
  }
`;

const WorkoutImage = styled.img`
  max-width: 80%;
  max-height: 80%;
  object-fit: cover;
  border-radius: 10px;

  @media (max-width: 480px) {
    max-width: 100%;
    max-height: 200px;
  }
`;
