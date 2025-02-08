import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import api from '../api/api';

const GymsPage = () => {
  const [gyms, setGyms] = useState([]);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchGyms = async () => {
      try {
        const response = await api.get('/gym'); // Запрос к API для получения списка залов
        setGyms(response.data);
      } catch (err) {
        console.error('Ошибка при загрузке залов:', err);
        setError('Ошибка при загрузке залов');
      }
    };

    fetchGyms();
  }, []);

  return (
    <PageContainer>
      <Header>
        <Title>Залы сети</Title>
      </Header>
      {error && <ErrorMessage>{error}</ErrorMessage>}
      <GymsContainer>
        {gyms.map((gym) => (
          <GymCard key={gym.id}>
            <GymInfo>
              <GymDetail><strong>Адрес:</strong> {gym.adress}</GymDetail>
              <GymDetail><strong>Часы работы:</strong> {gym.work_hours}</GymDetail>
              <GymDetail><strong>Телефон:</strong> {gym.phone}</GymDetail>
            </GymInfo>
          </GymCard>
        ))}
      </GymsContainer>
    </PageContainer>
  );
};

export default GymsPage;

// Styled components
const PageContainer = styled.div`
  background-color: #000;
  color: #fff;
  height: 100vh;
  display: flex;
  flex-direction: column;

  @media (max-width: 480px) {
    padding: 10px;
  }
`;

const Header = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #ff7b00;
  padding: 10px 20px;
  position: sticky;
  top: 0;
  z-index: 10;

  @media (max-width: 480px) {
    padding: 8px 15px;
  }
`;

const Title = styled.h1`
  font-size: 24px;

  @media (max-width: 480px) {
    font-size: 18px;
  }
`;

const ErrorMessage = styled.p`
  color: #ff4d4f;
  text-align: center;
  margin: 20px 0;

  @media (max-width: 480px) {
    font-size: 14px;
  }
`;

const GymsContainer = styled.div`
  flex: 1;
  overflow-y: auto;
  padding: 20px;

  @media (max-width: 480px) {
    padding: 10px;
  }
`;

const GymCard = styled.div`
  background-color: #f8f4f4;
  padding: 20px;
  margin-bottom: 10px;
  border-radius: 10px;
  display: flex;
  flex-direction: column;
  align-items: flex-start;

  @media (max-width: 480px) {
    padding: 15px;
  }
`;

const GymInfo = styled.div`
  display: flex;
  flex-direction: column;
  gap: 5px;
`;

const GymDetail = styled.p`
  margin: 0;
  color: #333;

  @media (max-width: 480px) {
    font-size: 14px;
  }
`;
