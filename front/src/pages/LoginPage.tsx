import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import { useNavigate } from 'react-router-dom';
import api from '../api/api';

const LoginPage = () => {
  const [form, setForm] = useState({
    email: '',
    password: '',
  });
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const navigate = useNavigate();

  // Восстанавливаем данные формы из localStorage
  useEffect(() => {
    const savedForm = localStorage.getItem('loginForm');
    if (savedForm) {
      setForm(JSON.parse(savedForm));
    }
  }, []);

  // Сохраняем данные формы в localStorage при каждом изменении
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    const updatedForm = { ...form, [name]: value };
    setForm(updatedForm);
    localStorage.setItem('loginForm', JSON.stringify(updatedForm)); // Сохраняем в localStorage
  };

  const handleLogin = async () => {
    try {
      setError('');
      setSuccess('');

      const response = await api.post('/login', form, {
        headers: { 'Content-Type': 'application/json; charset=utf-8' },
      });

      if (response.status === 200) {
        const userId = response.data.id;
        setSuccess('Авторизация прошла успешно!');
        setForm({ email: '', password: '' });
        localStorage.removeItem('loginForm'); // Очищаем localStorage при успешном логине

        setTimeout(() => {
          navigate('/mainmenu', { state: { userId } });
        }, 1000);
      }
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Ошибка авторизации');
    }
  };

  return (
    <PageContainer>
      <FormContainer>
        <Title>Авторизация</Title>
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
        <LoginButton onClick={handleLogin}>Войти</LoginButton>
        {error && <ErrorMessage>{error}</ErrorMessage>}
        {success && <SuccessMessage>{success}</SuccessMessage>}
        <Link href="/registration">Создать аккаунт</Link>
      </FormContainer>
    </PageContainer>
  );
};

export default LoginPage;

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

const LoginButton = styled.button`
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
