const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');

module.exports = {
  entry: './src/index.tsx',
  output: {
    path: path.resolve(__dirname, 'dist'),
    filename: 'bundle.js',
    clean: true, // Очищает папку dist перед сборкой
  },
  resolve: {
    extensions: ['.js', '.jsx', '.ts', '.tsx'], // Расширения для обработки
  },
  module: {
    rules: [
      {
        test: /\.(ts|tsx)$/, // Для файлов TypeScript и TSX
        use: 'babel-loader',
        exclude: /node_modules/,
      },
      {
        test: /\.(png|jpe?g|gif|svg)$/i, // Для обработки изображений
        type: 'asset/resource', // Включает обработку через встроенный Asset Modules
      },
    ],
  },
  plugins: [
    new HtmlWebpackPlugin({
      template: './public/index.html', // Путь до HTML-шаблона
    }),
  ],
  devServer: {
    static: './dist', // Папка для статики
    port: 8080, // Порт разработки
    hot: true, // Включает горячую перезагрузку
    historyApiFallback: true, // Перенаправление всех маршрутов на index.html
  },
};
