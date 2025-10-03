# Используем официальный образ Python 3.12
FROM python:3.12-slim AS builder

# Устанавливаем переменную окружения, чтобы Python не создавал .pyc файлы
ENV PYTHONDONTWRITEBYTECODE 1
# Устанавливаем переменную окружения, чтобы вывод Python был небуферизованным
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    python3-dev \
    libpq-dev \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

ADD pyproject.toml /app

RUN pip install --upgrade pip
RUN pip install poetry

RUN poetry install --no-root --no-interaction --no-ansi

# Копируем остальной код приложения (с учетом .dockerignore)
COPY . .

CMD ["poetry", "run", "uvicorn", "app.api.fast_api:create_app", "--host", "0.0.0.0", "--port", "7111"]
