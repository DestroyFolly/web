import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import api from '../api/api';

const TrainingsPage = () => {
  const [trainings, setTrainings] = useState([]);
  const [filteredTrainings, setFilteredTrainings] = useState([]);
  const [filter, setFilter] = useState('');

  useEffect(() => {
    const fetchTrainings = async () => {
      try {
        const response = await api.get('/trains'); // Запрос к API для получения списка тренировок
        setTrainings(response.data);
        setFilteredTrainings(response.data);
      } catch (err) {
        console.error('Ошибка при загрузке тренировок:', err);
      }
    };

    fetchTrainings();
  }, []);

  const handleFilterChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const selectedDay = e.target.value;
    setFilter(selectedDay);

    if (selectedDay) {
      const filtered = trainings.filter((training) =>
        training.dates.toLowerCase().includes(selectedDay.toLowerCase())
      );
      setFilteredTrainings(filtered);
    } else {
      setFilteredTrainings(trainings);
    }
  };

  return (
    <PageContainer>
      <Header>
        <Title>Тренировки</Title>
      </Header>
      <FilterContainer>
        <FilterLabel>Фильтр по дню недели:</FilterLabel>
        <FilterSelect value={filter} onChange={handleFilterChange}>
          <option value="">Все</option>
          <option value="monday">Monday</option>
          <option value="tuesday">Tuesday</option>
          <option value="wednesday">Wednesday</option>
          <option value="thursday">Thursday</option>
          <option value="friday">Friday</option>
          <option value="saturday">Saturday</option>
          <option value="sunday">Sunday</option>
        </FilterSelect>
      </FilterContainer>
      <TrainingsContainer>
        {filteredTrainings.length > 0 ? (
          filteredTrainings.map((training) => (
            <TrainingCard key={training.id}>
              <TrainingInfo>
                <TrainingName>{training.title}</TrainingName>
                <TrainingDetails>Time: {training.times}</TrainingDetails>
                <TrainingDetails>Dates: {training.dates}</TrainingDetails>
              </TrainingInfo>
            </TrainingCard>
          ))
        ) : (
          <NoTrainingsMessage>В данный день тренировок нет</NoTrainingsMessage>
        )}
      </TrainingsContainer>
    </PageContainer>
  );
};

export default TrainingsPage;

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
  padding: 10px 20px;

  @media (max-width: 480px) {
    padding: 10px;
  }
`;

const Title = styled.h1`
  font-size: 24px;

  @media (max-width: 480px) {
    font-size: 20px;
  }
`;

const FilterContainer = styled.div`
  display: flex;
  justify-content: flex-start;
  align-items: center;
  margin: 20px 0;

  @media (max-width: 480px) {
    flex-direction: column;
    align-items: flex-start;
    margin: 10px 0;
  }
`;

const FilterLabel = styled.label`
  margin-right: 10px;
  font-size: 16px;

  @media (max-width: 480px) {
    font-size: 14px;
    margin-bottom: 5px;
  }
`;

const FilterSelect = styled.select`
  padding: 5px 10px;
  border-radius: 5px;
  font-size: 16px;

  @media (max-width: 480px) {
    padding: 5px;
    font-size: 14px;
  }
`;

const TrainingsContainer = styled.div`
  display: flex;
  flex-direction: column;
  gap: 10px;
  height: 60vh;
  overflow-y: scroll;
  padding-right: 10px;

  @media (max-width: 480px) {
    height: auto;
    padding-right: 0;
  }
`;

const TrainingCard = styled.div`
  background-color: #f8f4f4;
  padding: 20px;
  border-radius: 10px;
  display: flex;
  flex-direction: column;
  align-items: flex-start;

  @media (max-width: 480px) {
    padding: 15px;
  }
`;

const TrainingInfo = styled.div`
  display: flex;
  flex-direction: column;
`;

const TrainingName = styled.h2`
  margin: 0;
  color: #000;

  @media (max-width: 480px) {
    font-size: 18px;
  }
`;

const TrainingDetails = styled.p`
  margin: 5px 0;
  color: #333;

  @media (max-width: 480px) {
    font-size: 14px;
  }
`;

const NoTrainingsMessage = styled.div`
  text-align: center;
  font-size: 18px;
  color: #ff4d4f;
  margin-top: 20px;

  @media (max-width: 480px) {
    font-size: 16px;
  }
`;
