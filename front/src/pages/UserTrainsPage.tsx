import React, { useEffect, useState } from 'react';
import styled from 'styled-components';
import api from '../api/api';
import { useLocation } from 'react-router-dom';
import avatar from '../assets/avatar.jpg';

const UserProfilePage = () => {
  const [user, setUser] = useState(null);
  const [error, setError] = useState('');
  const location = useLocation();

  // Получаем ID пользователя из состояния
  const userId = location.state?.userId;

  useEffect(() => {
    const fetchUser = async () => {
      try {
        const response = await api.get(`/users/${userId}`);
        setUser(response.data);
      } catch (err) {
        setError('Ошибка при загрузке данных пользователя.');
        console.error(err);
      }
    };

    if (userId) {
      fetchUser();
    }
  }, [userId]);

  if (error) {
    return (
      <PageContainer>
        <ErrorMessage>{error}</ErrorMessage>
      </PageContainer>
    );
  }

  if (!user) {
    return (
      <PageContainer>
        <LoadingMessage>Загрузка данных пользователя...</LoadingMessage>
      </PageContainer>
    );
  }

  return (
    <PageContainer>
      <Header>
        <Avatar src={avatar} alt="User Avatar" />
        <Title>Профиль</Title>
      </Header>
      <ProfileContainer>
        <ProfileField>
          <Label>Имя:</Label>
          <Value>{user.first_name}</Value>
        </ProfileField>
        <ProfileField>
          <Label>Фамилия:</Label>
          <Value>{user.surname}</Value>
        </ProfileField>
        <ProfileField>
          <Label>Email:</Label>
          <Value>{user.email}</Value>
        </ProfileField>
        <ProfileField>
          <Label>Телефон:</Label>
          <Value>{user.phone}</Value>
        </ProfileField>
      </ProfileContainer>
    </PageContainer>
  );
};

export default UserProfilePage;

// Styled Components
const PageContainer = styled.div`
  background-color: #000;
  color: #fff;
  height: 100vh;
  padding: 0;

  @media (max-width: 480px) {
    padding: 10px;
  }
`;

const Header = styled.div`
  background-color: #ff7b00;
  padding: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;

  @media (max-width: 480px) {
    padding: 15px;
  }
`;

const Avatar = styled.img`
  width: 100px;
  height: 100px;
  border-radius: 50%;
  margin-bottom: 10px;
  border: 3px solid #fff;

  @media (max-width: 480px) {
    width: 80px;
    height: 80px;
  }
`;

const Title = styled.h1`
  font-size: 24px;
  color: #fff;
  margin: 0;

  @media (max-width: 480px) {
    font-size: 20px;
  }
`;

const ProfileContainer = styled.div`
  margin-top: 20px;
  display: flex;
  flex-direction: column;
  gap: 20px;
  padding: 20px;

  @media (max-width: 480px) {
    padding: 10px;
  }
`;

const ProfileField = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #333;
  padding: 10px;
  border-radius: 10px;

  @media (max-width: 480px) {
    padding: 8px;
  }
`;

const Label = styled.span`
  font-weight: bold;
  font-size: 18px;

  @media (max-width: 480px) {
    font-size: 16px;
  }
`;

const Value = styled.span`
  font-size: 18px;

  @media (max-width: 480px) {
    font-size: 16px;
  }
`;

const ErrorMessage = styled.p`
  color: red;
  text-align: center;
  font-size: 18px;

  @media (max-width: 480px) {
    font-size: 16px;
  }
`;

const LoadingMessage = styled.p`
  color: #fff;
  text-align: center;
  font-size: 18px;

  @media (max-width: 480px) {
    font-size: 16px;
  }
`;
