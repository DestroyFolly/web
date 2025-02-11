# Используем Node.js
FROM node:18
WORKDIR /app

# Копируем package.json и устанавливаем зависимости
COPY package.json package-lock.json ./
RUN npm install

# Копируем весь проект
COPY . ./

# Открываем порт 5173 (Vite)
EXPOSE 5173

# Запускаем frontend через npm run dev
CMD ["npm", "run", "dev", "--", "--host"]
