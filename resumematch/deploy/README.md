# Deploy

- docker-compose.yml для локального PoC
- k8s/ манифесты для демонстрации прод-схемы
- env/ переменные окружения

## Окружения

- Шаблон: `.env.example` — скопируйте и измените значения.
- Dev: `env/.env.dev`
- Prod: `env/.env.prod`

## Запуск

- Development:
  - `cd resumematch/deploy`
  - `docker compose --env-file env/.env.dev up --build`

- Production (пример):
  - `cd resumematch/deploy`
  - `docker compose --env-file env/.env.prod -f docker-compose.yml up -d`

При интерполяции `${VAR}` Compose берёт значения из: shell → `--env-file` → `.env` → системные переменные.