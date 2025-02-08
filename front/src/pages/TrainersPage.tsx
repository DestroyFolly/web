import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import api from '../api/api';

const TrainersPage = () => {
  const [trainers, setTrainers] = useState([]);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchTrainers = async () => {
      try {
        setError('');
        const response = await api.get('/trainers'); // Используем базовый URL из api
        setTrainers(response.data);
      } catch (err: any) {
        setError(err.response?.data?.detail || 'Ошибка при загрузке тренеров');
      }
    };

    fetchTrainers();
  }, []);

  return (
    <PageContainer>
      <Header>
        <Title>Тренеры</Title>
      </Header>
      {error ? (
        <ErrorMessage>{error}</ErrorMessage>
      ) : (
        <TrainersContainer>
          {trainers.map((trainer) => (
            <TrainerCard key={trainer.id}>
              <TrainerInfo>
                <TrainerName>{trainer.first_name} {trainer.surname}</TrainerName>
                <TrainerPhone>Phone number: {trainer.number}</TrainerPhone>
              </TrainerInfo>
            </TrainerCard>
          ))}
        </TrainersContainer>
      )}
    </PageContainer>
  );
};

export default TrainersPage;

// Styled components
const PageContainer = styled.div`
  background-color: #000;
  color: #fff;
  height: 100vh;
  padding: 20px;

  @media (max-width: 480px) {
    padding: 10px;
  }
`;

const Header = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #ff7b00;
  padding: 0 20px;
  height: 60px;

  @media (max-width: 480px) {
    height: 50px;
  }
`;

const Title = styled.h1`
  font-size: 18px;

  @media (max-width: 480px) {
    font-size: 16px;
  }
`;

const TrainersContainer = styled.div`
  padding: 20px;

  @media (max-width: 480px) {
    padding: 10px;
  }
`;

const TrainerCard = styled.div`
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

const TrainerInfo = styled.div`
  display: flex;
  flex-direction: column;
`;

const TrainerName = styled.h2`
  margin: 0;
  color: #000;

  @media (max-width: 480px) {
    font-size: 16px;
  }
`;

const TrainerPhone = styled.p`
  margin: 5px 0 0;
  color: #555;

  @media (max-width: 480px) {
    font-size: 14px;
  }
`;

const ErrorMessage = styled.p`
  color: #ff4d4f;
  text-align: center;
  margin-top: 20px;
  font-size: 14px;

  @media (max-width: 480px) {
    font-size: 12px;
  }
`;
