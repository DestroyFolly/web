import axios from 'axios';

// Мокируем axios
jest.mock('axios');

// Создаем мок-объект для axios.create
const mockedAxiosInstance = {
  get: jest.fn(),
  post: jest.fn(),
  interceptors: {
    request: { use: jest.fn(), eject: jest.fn() },
    response: { use: jest.fn(), eject: jest.fn() },
  },
};

// Заменяем реализацию axios.create, чтобы возвращать мок-объект
(axios.create as jest.Mock).mockReturnValue(mockedAxiosInstance);

// Импортируем api после мокирования axios
import api from '../src/api/api';

describe('API tests', () => {
  test('fetches trainings from API', async () => {
    mockedAxiosInstance.get.mockResolvedValueOnce({ data: [{ id: 1, title: 'Aerobics' }] });

    const response = await api.get('/trains');

    expect(response.data).toEqual([{ id: 1, title: 'Aerobics' }]);
    expect(mockedAxiosInstance.get).toHaveBeenCalledWith('/trains');
  });

  test('fetches gyms from API', async () => {
    mockedAxiosInstance.get.mockResolvedValueOnce({ data: [{ id: 1, name: 'Main Gym' }] });

    const response = await api.get('/gyms');

    expect(response.data).toEqual([{ id: 1, name: 'Main Gym' }]);
    expect(mockedAxiosInstance.get).toHaveBeenCalledWith('/gyms');
  });

  test('fetches trainers from API', async () => {
    mockedAxiosInstance.get.mockResolvedValueOnce({ data: [{ id: 1, name: 'John Doe' }] });

    const response = await api.get('/trainers');

    expect(response.data).toEqual([{ id: 1, name: 'John Doe' }]);
    expect(mockedAxiosInstance.get).toHaveBeenCalledWith('/trainers');
  });

  test('handles API error gracefully', async () => {
    mockedAxiosInstance.get.mockRejectedValueOnce(new Error('Network Error'));

    await expect(api.get('/trains')).rejects.toThrow('Network Error');
  });

  test('registers a user successfully', async () => {
    const userData = { email: 'test@example.com', password: '12345' };
    mockedAxiosInstance.post.mockResolvedValueOnce({ status: 201, data: { id: 1, ...userData } });

    const response = await api.post('/register', userData);

    expect(response.status).toBe(201);
    expect(response.data).toEqual({ id: 1, ...userData });
    expect(mockedAxiosInstance.post).toHaveBeenCalledWith('/register', userData);
  });

  test('logs in a user successfully', async () => {
    const loginData = { email: 'test@example.com', password: '12345' };
    mockedAxiosInstance.post.mockResolvedValueOnce({ status: 200, data: { token: 'abc123' } });

    const response = await api.post('/login', loginData);

    expect(response.status).toBe(200);
    expect(response.data).toEqual({ token: 'abc123' });
    expect(mockedAxiosInstance.post).toHaveBeenCalledWith('/login', loginData);
  });

  test('fetches user profile', async () => {
    mockedAxiosInstance.get.mockResolvedValueOnce({ data: { id: 1, name: 'John Doe', email: 'test@example.com' } });

    const response = await api.get('/users/1');

    expect(response.data).toEqual({ id: 1, name: 'John Doe', email: 'test@example.com' });
    expect(mockedAxiosInstance.get).toHaveBeenCalledWith('/users/1');
  });
});
