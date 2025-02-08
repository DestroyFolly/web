import type { Config } from 'jest';

const config: Config = {
  clearMocks: true,
  coverageProvider: "v8",
  testEnvironment: "jsdom",
  roots: ["<rootDir>/tests"], // Указываем папку с тестами
  testMatch: [
    "**/?(*.)+(spec|test).[tj]s?(x)",
    "**/tests.tsx", // Поддержка вашего файла
  ],
  moduleFileExtensions: ["js", "jsx", "ts", "tsx", "json", "node"],
  transform: {
    "^.+\\.tsx?$": "ts-jest", // Используем ts-jest для трансформации TypeScript
  },
};

export default config;
