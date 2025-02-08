import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import { useNavigate } from 'react-router-dom';
import api from '../api/api'; // Импорт API

const RegistrationPage = () => {
  const [form, setForm] = useState({
    first_name: '',
    surname: '',
    phone: '',
    email: '',
    password: '',
    gender: 'M', // Значение по умолчанию
  });
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const navigate = useNavigate();

  // Восстанавливаем данные формы из localStorage, если они есть
  useEffect(() => {
    const savedForm = localStorage.getItem('registrationForm');
    if (savedForm) {
      setForm(JSON.parse(savedForm));
    }
  }, []);

  // Сохраняем данные формы в localStorage при каждом изменении
  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    const updatedForm = { ...form, [name]: value };
    setForm(updatedForm);
    localStorage.setItem('registrationForm', JSON.stringify(updatedForm)); // Сохраняем в localStorage
  };

  const handleRegister = async () => {
    try {
      setError('');
      setSuccess('');

      const cleanedForm = {
        ...form,
        phone: parseInt(form.phone.replace(/\D/g, ''), 10),
      };

      const response = await api.post(
        '/register',
        cleanedForm,
        {
          headers: { 'Content-Type': 'application/json; charset=utf-8' },
        }
      );

      if (response.status === 201) {
        setSuccess('Регистрация прошла успешно!');
        localStorage.removeItem('registrationForm'); // Очищаем localStorage при успешной регистрации

        const userId = response.data.id;

        // Перенаправление на страницу MainMenu с передачей ID
        setTimeout(() => navigate('/mainmenu', { state: { userId } }), 1000);
      }
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Ошибка регистрации');
    }
  };

  return (
    <PageContainer>
      <FormContainer>
        <Title>Регистрация</Title>
        <Input
          type="text"
          name="first_name"
          placeholder="Имя"
          value={form.first_name}
          onChange={handleChange}
        />
        <Input
          type="text"
          name="surname"
          placeholder="Фамилия"
          value={form.surname}
          onChange={handleChange}
        />
        <Input
          type="number"
          name="phone"
          placeholder="Номер телефона"
          value={form.phone}
          onChange={handleChange}
        />
        <Input
          type="email"
          name="email"
          placeholder="Почта"
          value={form.email}
          onChange={handleChange}
        />
        <Input
          type="password"
          name="password"
          placeholder="Пароль"
          value={form.password}
          onChange={handleChange}
        />
        <Select
          name="gender"
          value={form.gender}
          onChange={handleChange}
        >
          <option value="M">М</option>
          <option value="F">Ж</option>
        </Select>
        <RegisterButton onClick={handleRegister}>Зарегистрироваться</RegisterButton>
        {error && <ErrorMessage>{error}</ErrorMessage>}
        {success && <SuccessMessage>{success}</SuccessMessage>}
        <Link href="/login">Уже есть аккаунт?</Link>
      </FormContainer>
    </PageContainer>
  );
};

export default RegistrationPage;

// Styled Components
const PageContainer = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
  background-color: #000;
  padding: 10px;
`;

const FormContainer = styled.div`
  background-color: #333;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.5);
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 90%;
  max-width: 400px;

  @media (max-width: 480px) {
    padding: 15px;
    max-width: 90%;
  }
`;

const Title = styled.h1`
  color: #fff;
  margin-bottom: 20px;
  font-size: 24px;

  @media (max-width: 480px) {
    font-size: 20px;
  }
`;

const Input = styled.input`
  width: 100%;
  padding: 10px;
  margin-bottom: 15px;
  border: none;
  border-radius: 5px;
  font-size: 16px;

  @media (max-width: 480px) {
    padding: 8px;
    font-size: 14px;
  }
`;

const Select = styled.select`
  width: 100%;
  padding: 10px;
  margin-bottom: 15px;
  border: none;
  border-radius: 5px;
  font-size: 16px;

  @media (max-width: 480px) {
    padding: 8px;
    font-size: 14px;
  }
`;

const RegisterButton = styled.button`
  width: 100%;
  padding: 10px;
  background-color: #ff7b00;
  color: #fff;
  border: none;
  border-radius: 5px;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.3s;

  &:hover {
    background-color: #e67000;
  }

  @media (max-width: 480px) {
    padding: 8px;
    font-size: 14px;
  }
`;

const ErrorMessage = styled.p`
  color: #ff4d4f;
  margin-top: 10px;
  text-align: center;
  font-size: 14px;

  @media (max-width: 480px) {
    font-size: 12px;
  }
`;

const SuccessMessage = styled.p`
  color: #4caf50;
  margin-top: 10px;
  text-align: center;
  font-size: 14px;

  @media (max-width: 480px) {
    font-size: 12px;
  }
`;

const Link = styled.a`
  color: #ff7b00;
  margin-top: 10px;
  text-decoration: none;
  font-size: 16px;

  &:hover {
    text-decoration: underline;
  }

  @media (max-width: 480px) {
    font-size: 14px;
  }
`;
