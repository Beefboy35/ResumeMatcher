# ResumeMatchEDU Monorepo

Структура и слои проекта согласно документу архитектуры.

- apps/backend: Django + GraphQL (Strawberry) + DRF, слои core/application/interface/infrastructure/di
- apps/frontend: React + TypeScript, слои core/application/presentation/infrastructure/di
- shared: общие контракты и утилиты
- deploy: Docker Compose и Kubernetes манифесты
- Makefile: команды для разработки и сборки