import axios from 'axios';

// Создаем экземпляр axios с базовой конфигурацией
const api = axios.create({
  baseURL: 'http://127.0.0.1:8009', // Убедитесь, что это правильный адрес сервера
  timeout: 10000, // Таймаут для запросов в миллисекундах
});

// Обработчик запросов (можно добавить токены и другие заголовки здесь)
api.interceptors.request.use(
  (config) => {
    // Если нужен токен, можно добавить его в заголовки здесь
    // Например: config.headers.Authorization = `Bearer ${token}`;
    return config;
  },
  (error) => {
    // Логировать ошибку запроса
    console.error('Request Error:', error);
    return Promise.reject(error);
  }
);

// Обработчик ответов (можно обрабатывать ошибки API здесь)
api.interceptors.response.use(
  (response) => {
    // Здесь можно обработать успешные ответы
    return response;
  },
  (error) => {
    // Логировать ошибки ответа
    console.error('Response Error:', error.response || error.message);
    return Promise.reject(error);
  }
);

export default api;
