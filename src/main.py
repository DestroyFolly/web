import requests

url = 'http://localhost/mirror1/train'
response = requests.get(url)

# Проверим заголовки
print(response.headers)
