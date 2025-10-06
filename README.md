ФИНАМ Радар финансовых новостей

Кратко
- **Что это**: система мониторинга и аналитики финансовых новостей и рыночных данных для компании «ФИНАМ».
- **Задача**: собирать новости из источников (Telegram, RSS/медиа), нормализовать, сохранять, дополнять рыночными данными (MOEX/Yahoo), рассчитывать «горячесть» повестки и отдавать удобный API и веб‑интерфейс.
- **Стек**: FastAPI, Celery, Redis, PostgreSQL, ClickHouse, ChromaDB, Alembic, Python 3.11+, Next.js (client), Tailwind, OpenRouter LLM.

Состав проекта
- `app_analytics` — сервис API/аналитики (FastAPI):
  - публичные и внутренние эндпоинты `api/v1/public` и `api/v1/internal`;
  - интеграции с ClickHouse, ChromaDB;
  - юзкейсы обработки данных, сохранения новостей, тикеров и рыночных метрик;
  - Alembic‑миграции для PostgreSQL в каталоге `alembic/`.
- `app_parsing` — сервис парсинга:
  - планировщик и воркер Celery (с Redis);
  - парсеры источников (`parsers/`): Telegram, Интерфакс, РБК, RSS MOEX и др.;
  - интеграция с `app_analytics` через внутренний API.
- `client` — фронтенд (Next.js): чат‑интерфейс и компоненты визуализации новостей/«горячести».

Архитектура и данные
- Хранилища:
  - PostgreSQL — транзакционные данные, события, тикеты.
  - ClickHouse — агрегированные рыночные данные и быстрая аналитика.
  - ChromaDB — векторное хранилище для семантических запросов/поиска.
- Очереди и фоновые задачи: Celery + Redis.
- LLM: OpenRouter (модель и ключ берутся из переменных окружения) — генерация текстов/обогащение.

Быстрый старт (Docker Compose)
1) Подготовьте `.env` в корне проекта (см. раздел «Переменные окружения»).
2) Запустите инфраструктуру и сервисы:
```bash
docker compose -f docker-compose.local.yml up -d --build
```
3) После старта будут доступны:
- Backend API: `http://localhost:8000/api/v1` (Swagger — `http://localhost:8000/docs`).
- ClickHouse HTTP: `http://localhost:8123`.
- ChromaDB: `http://localhost:8001`.
- Redis: `localhost:6379`.

Миграции БД
- Применяются автоматически при старте контейнера `app`:
  `poetry run alembic upgrade head`.
- Для ручного запуска внутри контейнера `app`:
```bash
docker compose -f docker-compose.local.yml exec app poetry run alembic upgrade head
```

Переменные окружения (.env)
Обязательные для `app_analytics`:
- `LOG_LEVEL` — уровень логирования (например, `INFO`).
- PostgreSQL: `POSTGRES_HOST`, `POSTGRES_PORT`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`.
- ClickHouse: `CLICKHOUSE_HOST`, `CLICKHOUSE_PORT` (8123), `CLICKHOUSE_DB`, `CLICKHOUSE_USER`, `CLICKHOUSE_PASSWORD`.
- ChromaDB: `CHROMA_HOST`, `CHROMA_PORT`, `CHROMA_IS_PERSISTENT` (TRUE/FALSE).
- OpenRouter: `OPEN_ROUTER_API_KEY`, `OPEN_ROUTER_MODEL`, `OPEN_ROUTER_URL`.
- Внутренний доступ: `INTERNAL_API_TOKEN` — Bearer‑токен для `/api/v1/internal/*`.

Для `app_parsing` (парсер/воркер Celery):
- Redis: `REDIS_HOST` (по умолчанию `redis`), `REDIS_PORT` (6379).
- Telegram: `TELEGRAM_API_ID`, `TELEGRAM_API_HASH`, `TELEGRAM_TOKEN`.
- Каналы: `TELEGRAM_CHANNELS` (через запятую или список в `.env`).
- Тот же `INTERNAL_API_TOKEN` для обращения к внутренним эндпоинтам `app_analytics`.

Сервисы и порты в docker-compose.local.yml
- `chroma` — ChromaDB, порт `8001` (проброшен на 8000 сервиса).
- `postgres` — PostgreSQL 15, порт `5432`.
- `clickhouse` — ClickHouse 23, порты `9000` (native), `8123` (HTTP).
- `app` — FastAPI (`app_analytics`), порт `8000`, автоприменение миграций и запуск `uvicorn`.
- `redis` — Redis 7, порт `6379`.
- `celery_worker` — Celery‑воркер для парсинга (`app_parsing`).

Frontend (client)
- Переменные окружения клиента (см. `client/README.md`):
  - `OPENROUTER_API_KEY` — ключ OpenRouter (на клиентской стороне используйте прокси/бэкенд по возможности).
  - `SERVER_URL` — адрес публичного API, например `http://localhost:8000/api/v1/public/`.
- Локальный запуск в Docker (из каталога `client/`):
```bash
docker build -t finam-client:prod .
docker run -p 3000:3000 finam-client:prod
# либо режим разработки:
docker build --target development -t finam-client:dev .
docker run -p 3000:3000 finam-client:dev
```

API обзор (основные маршруты)
Базовый префикс: `/api/v1`.
- Публичные:
  - `POST /public/generate/` — генерация текста (LLM); схема в `public/schemas/generation.py`.
- Внутренние (требуют `Authorization: Bearer <INTERNAL_API_TOKEN>`):
  - `GET /internal/tickets/` — список тикеров компаний.
  - `POST /internal/news/` — сохранение новости (заголовок, тело, время, источник, URL).
  - `POST /internal/market_data/` — добавление рыночных данных.

Разработка без Docker (быстрый набросок)
1) Python 3.11+, Poetry:
```bash
poetry install
poetry run alembic upgrade head
poetry run uvicorn app_analytics.api.fast_api:create_app --host 0.0.0.0 --port 8000 --reload --no-access-log
```
2) Отдельно запустите ClickHouse, PostgreSQL, Redis, ChromaDB и настройте `.env` под локальные адреса.

Тесты
- Примеры и фикстуры находятся в `tests/` и `test/`.

Полезные ссылки
- Документация Swagger: `http://localhost:8000/docs`.
- OpenAPI JSON: `http://localhost:8000/openapi.json`.

Лицензия
- Внутренний проект для хакатона/прототипирования в рамках компании «ФИНАМ».


