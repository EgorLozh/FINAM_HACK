## Запуск докера

ENV:
```bash
OPENROUTER_API_KEY=''
SERVER_URL='http://localhost:8000/api/v1/public/'
```

Для Прода:
```bash
docker build -t finam-client:prod .

docker run -p 3000:3000 finam-client:prod
```

Для Теста:
```bash
docker build --target development -t finam-client:dev .

docker run -p 3000:3000 finam-client:dev
```