# ResumeMatchEDU – Архитектура (PoC)  
Версия: 0.1

---

## 1. ЦЕЛЬ ПРОЕКТА

ResumeMatchEDU – учебный проект (Proof of Concept), который автоматически подбирает кандидатов под текст вакансии (Job Description, JD).  
Система формирует короткий список (shortlist), объясняет, почему кандидат подходит, и позволяет рекрутеру давать метки ("подходит / не подходит / позже") для дообучения качества.

**Ключевые задачи:**
- быстрый матчинг кандидатов по вакансии;
- прозрачная объяснимость (навыки, совпадения терминов);
- сбор обратной связи для улучшения модели;
- минимальный фронтенд (3 экрана) и воспроизводимая архитектура.

---

## 2. ОБЩАЯ АРХИТЕКТУРА

Система состоит из:

1. **Frontend (React + TypeScript)**  
2. **Backend (Django + GraphQL + DRF)**  
3. **ML-модуль (scikit-learn)**  
4. **Хранилища данных (Postgres + MongoDB GridFS)**  
5. **Инфраструктура (Docker Compose / Kubernetes)**

Frontend и Backend живут в одном монорепозитории и оба построены по принципам:
- Чистой архитектуры (Clean Architecture)
- Inversion of Control / Dependency Inversion
- Dependency Injection (DI)

### 2.1 Компоненты

**Frontend:**
- SPA с 3 экранами:
  - `CandidatesList`: список кандидатов, отсортированных по score
  - `CandidateDetail`: объяснимость (совпавшие навыки, чего не хватает)
  - `UploadPage`: загрузка резюме и/или создание вакансии
- Общается с Backend через GraphQL (матчинг, метки) и REST (загрузка файлов).

**Backend:**
- GraphQL (Strawberry): доменные use case-операции (`match`, `labelCandidate`, получить кандидата)
- DRF: работа с файлами (`upload`/`download`), экспорт CSV
- ML ядро: tf-idf индекс кандидатов, косинусное сходство, простые правила по навыкам/опыту/локации

**Хранилища:**
- Postgres: кандидаты, вакансии, метки, связи
- MongoDB (GridFS): бинарные файлы резюме/JD и бинарные артефакты модели (`joblib`)

**Инфраструктура:**
- Docker Compose для PoC
- Kubernetes (namespace `resumematch`) для демонстрации продоподобной поставки

---

## 3. СТРУКТУРА МОНОРЕПОЗИТОРИЯ

```text
resumematch/
  apps/
    backend/
      src/
        core/                # Domain layer (Entities, Value Objects, Ports)
        application/         # Use Cases / Interactors
        interface/           # GraphQL resolvers, DRF views (контроллеры)
        infrastructure/      # Реализации портов: ORM, GridFS, tf-idf matcher
        di/                  # DI-контейнер и связывание зависимостей
    frontend/
      src/
        core/                # Domain layer (Entities, Types, Ports)
        application/         # Use Cases (hooks / сервисы бизнес-логики)
        presentation/        # React-компоненты и страницы
        infrastructure/      # API-клиенты (GraphQL client, REST upload client)
        di/                  # DI-провайдеры через React context
    shared/
      contracts/             # Общие DTO, схемы запросов/ответов
      utils/                 # Общие константы, формат логов
      docs/                  # Документация и ADR

  deploy/
    docker-compose.yml
    k8s/                     # Манифесты для api, frontend, postgres, mongodb
    env/
      dev.env
      prod.env

  Makefile
```

Смысл: фронт и бэк делят одни и те же доменные контракты (типовки/DTO), но остаются слабо связаны через порты/интерфейсы.

---

## 4. СЛОИ И ЗАВИСИМОСТИ (CLEAN ARCHITECTURE + DI)

Общая идея чистой архитектуры:
- Самые внутренние слои (домен) ничего не знают про фреймворки, БД, HTTP, React, Django.
- Внешние слои знают о внутренних.
- Внедрение зависимостей (DI): конкретные реализации интерфейсов подставляются снаружи при старте приложения.

Слои (от центра к периферии):
1. **Core / Domain**
2. **Application / Use Cases**
3. **Interface** (на бэкенде) или **Presentation** (на фронтенде)
4. **Infrastructure**
5. **DI-слой как точка сборки**

Зависимости направлены внутрь: наружные зависят от внутренних, но не наоборот.

### 4.1 Общая схема слоёв

```text
(внешний мир: HTTP, UI, DB, ML-модель)

         +-----------------------------+
         | Interface / Presentation    |   <-- React pages / GraphQL resolvers / DRF views
         +--------------▲--------------+
                        | вызывает
         +--------------▼--------------+
         | Application / Use Cases     |   <-- бизнес-сценарии (matchVacancy, labelCandidate)
         +--------------▲--------------+
                        | требует абстрактные порты
         +--------------▼--------------+
         | Core / Domain               |   <-- сущности, value objects, контракты портов
         +--------------▲--------------+
                        | реализуется адаптерами
         +--------------▼--------------+
         | Infrastructure Adapters     |   <-- PostgresRepo, MongoGridFS, SklearnMatcher
         +-----------------------------+

DI связывает Use Case с конкретной реализацией портов из Infrastructure.
```

---

### 4.2 Backend

#### 4.2.1 Core (`backend/src/core/`)
- Доменные сущности:
  - `Candidate`
  - `Vacancy`
  - `MatchScore`
  - `LabelDecision`
- Value Objects:
  - `SkillsSet`
  - `ExperienceYears`
  - `Location`
- Порты (абстрактные интерфейсы, чистый Python):
  - `CandidateRepoPort`
  - `VacancyRepoPort`
  - `LabelRepoPort`
  - `MatcherPort` (`match(vacancyText) -> список MatchScore`)
  - `FileStoragePort` (`put_file`, `get_file`)

Core не знает о Django, базе, HTTP, scikit-learn.

#### 4.2.2 Application (`backend/src/application/`)
- Use Cases:
  - `MatchVacancyUseCase`
    - получает `vacancyId`
    - тянет JD вакансии через `VacancyRepoPort`
    - вызывает `MatcherPort`
    - подготавливает DTO ответа
  - `LabelCandidateUseCase`
    - валидирует вход
    - пишет в `LabelRepoPort` (`vacancyId`, `candidateId`, `label`)
    - (опционально) сигнализирует о новом обучающем примере

Use case не знает, Postgres это или что-то ещё.

#### 4.2.3 Interface (`backend/src/interface/`)
- **GraphQL резолверы (Strawberry):**
  - `Query.match(vacancyId, topK)`
  - `Mutation.labelCandidate(vacancyId, candidateId, label)`
- **DRF views:**
  - `POST /api/upload` → загрузка резюме или JD
  - `GET /api/download/{file_id}`
  - `GET /api/export.csv` (опционально)

Эти контроллеры только вызывают Use Case.

#### 4.2.4 Infrastructure (`backend/src/infrastructure/`)
Реализации портов:
- `DjangoORMCandidateRepo` implements `CandidateRepoPort`
- `DjangoORMVacancyRepo` implements `VacancyRepoPort`
- `DjangoORMLabelRepo` implements `LabelRepoPort`
- `MongoGridFSFileStorage` implements `FileStoragePort` (использует MongoDB GridFS)
- `SklearnTfidfMatcher` implements `MatcherPort`
  - загружает артефакты tf-idf (joblib) из MongoDB GridFS
  - держит их в памяти
  - считает косинусное сходство
  - добавляет бизнес-правила (совпадение навыков, опыт, локация)

#### 4.2.5 DI backend (`backend/src/di/`)
- Контейнер зависимостей, который:
  - создаёт подключения к Postgres и MongoDB
  - создаёт объекты репозиториев
  - создаёт объект `SklearnTfidfMatcher`
  - создаёт экземпляры Use Case (`MatchVacancyUseCase`, `LabelCandidateUseCase`)
  - прокидывает их в резолверы GraphQL и DRF views

Django не создаёт use case напрямую: он получает уже собранный экземпляр через DI.

---

### 4.3 Frontend

#### 4.3.1 Core (`frontend/src/core/`)
- Доменные типы/модели в TypeScript:
  - `Candidate { id, fullName, location, yearsExp, skills, score ... }`
  - `Vacancy { id, title, jdText ... }`
  - `MatchResult { items: Candidate[], total, vacancyId }`
- Порты (TS интерфейсы):
  - `MatchServicePort { match(vacancyId: string): Promise<MatchResult> }`
  - `LabelServicePort { label(vacancyId, candidateId, label): Promise<void> }`
  - `UploadServicePort { uploadResume(file): Promise<{candidateId: string}> }`

Core фронтенда не знает, GraphQL это или REST.

#### 4.3.2 Application (`frontend/src/application/`)
Бизнес-хуки и сервисы состояния:
- `useMatchVacancy(vacancyId)`
  - обращается к `MatchServicePort`
  - возвращает данные для `CandidatesListPage`
- `useLabelCandidate()`
  - дергает `LabelServicePort`
  - возвращает функцию `mark("pos" | "neg" | "later")`
- `useUploadResume()`
  - дергает `UploadServicePort`
  - управляет формой загрузки файла

Эти хуки не знают о transport layer (Apollo, fetch и т.д.).

#### 4.3.3 Presentation (`frontend/src/presentation/`)
React-компоненты и страницы:
- `CandidatesListPage`
- `CandidateDetailPage`
- `UploadPage`

Ответственность: отрисовать данные, не содержать бизнес-логику матчинга.

#### 4.3.4 Infrastructure (`frontend/src/infrastructure/`)
Реальные клиенты:
- `GraphQLMatchService` implements `MatchServicePort`
- `GraphQLLabelService` implements `LabelServicePort`
- `RestUploadService` implements `UploadServicePort`
  - делает `POST /api/upload` для отправки PDF/DOCX

Если меняется транспорт (например, уходим от Apollo), Presentation и Application не ломаются — меняется только Infrastructure.

#### 4.3.5 DI frontend (`frontend/src/di/`)
- `ServiceContainerContext` (React Context):
  - В него кладутся реализации портов: `GraphQLMatchService`, `GraphQLLabelService`, `RestUploadService`
- Провайдер оборачивает всё приложение.
- Хуки Application достают конкретные сервисы через этот контекст.
- Это и есть Dependency Injection на фронте.

---

## 5. ПОТОК ДАННЫХ: MATCH

Сценарий: рекрутер хочет получить лучших кандидатов под вакансию.

1. Пользователь в UI открывает страницу подбора (`CandidatesListPage`).
2. Presentation вызывает `useMatchVacancy(vacancyId)`.
3. `useMatchVacancy` обращается к `MatchServicePort.match()`.
4. `MatchServicePort` реализован `GraphQLMatchService` → отправляет GraphQL-запрос `{ match(vacancyId) }`.
5. На бэкенде GraphQL-резолвер `MatchResolver` (слой Interface) вызывает `MatchVacancyUseCase`.
6. `MatchVacancyUseCase` (слой Application) тянет текст вакансии через `VacancyRepoPort` и вызывает `MatcherPort`.
7. `SklearnTfidfMatcher` (слой Infrastructure) использует tf-idf артефакты, считает косинусную близость, добавляет правила по навыкам/опыту/локации, возвращает топ-кандидатов.
8. Use Case упаковывает DTO `MatchResult` и возвращает его резолверу.
9. Резолвер отдаёт JSON фронтенду.
10. Хук `useMatchVacancy` получает результат и даёт данные `CandidatesListPage`.
11. Страница рендерит таблицу кандидатов по score.

Ни фронт, ни Use Case не знают про конкретную БД или ML-библиотеку — только про абстрактные порты.

---

## 6. ХРАНИЛИЩА ДАННЫХ

### 6.1 Postgres
Хранит структурированные сущности и связи:

- `candidate(id, full_name, contact_email, location, years_exp, skills_json, resume_file_id, created_at)`
- `vacancy(id, title, location, skills_req_json, jd_file_id, created_at)`
- `label(id, vacancy_id, candidate_id, label ENUM('pos','neg','later'), reason, created_at)`

**Почему Postgres:**
- чёткие связи (`candidate ↔ vacancy` через `label`)
- удобные выборки для аналитики и истории решений

### 6.2 MongoDB GridFS
Хранит:
- исходные файлы резюме / JD (PDF/DOCX)
- извлечённые тексты (при желании)
- артефакты модели (joblib):  
  - `tfidf` векторизатор  
  - `candidates_csr` (разреженная матрица резюме)  
  - `candidate_ids` (индексы → id в Postgres)

**Почему MongoDB GridFS:**
- удобно сохранять бинарные блобы без поднятия S3/MinIO
- хранение версий артефактов модели
- простое скачивание файла по `file_id`

---

## 7. ДЕПЛОЙ

### 7.1 Docker Compose (PoC)
Сервисы:
- `frontend` (React статика + nginx)
- `api` (Django ASGI: GraphQL + DRF)
- `postgres`
- `mongodb`

Цель: быстрый локальный запуск.

### 7.2 Kubernetes (демо продовой схемы)
- Namespace: `resumematch`
- Deployments:
  - `api` (Django)
  - `frontend` (статический фронт)
- StatefulSets:
  - `postgres` (PVC)
  - `mongodb` (PVC)
- Secret `app-secrets`:
  - строки подключения к Postgres и MongoDB
  - `DJANGO_SECRET_KEY`
- Ingress:
  - `/` → frontend service
  - `/api/` → api service
- (опционально) `CronJob retrain`:
  - ночной пересчёт tf-idf индекса и обновление артефактов в MongoDB

---

## 8. ИНВЕРСИЯ ЗАВИСИМОСТЕЙ И DI

**Dependency Inversion:**
- Use Case слоя (Application) зависит не от конкретной реализации репозитория или матчера, а от абстрактного интерфейса (порт).
- Конкретная реализация живёт в Infrastructure и подаётся (inject) снаружи через DI.

**Dependency Injection:**
- Backend:
  - При старте Django создаётся контейнер зависимостей.
  - Контейнер инициализирует репозитории (Postgres), хранение файлов (MongoDB GridFS) и ML-модуль (`SklearnTfidfMatcher`).
  - Контейнер создаёт экземпляры Use Case.
  - GraphQL резолверы и DRF views получают готовые Use Case из контейнера.
- Frontend:
  - В корневом React-провайдере (`ServiceContainerProvider`) создаются клиенты для GraphQL и REST.
  - Эти клиенты реализуют порты `MatchServicePort`, `LabelServicePort`, `UploadServicePort`.
  - Хуки бизнес-логики используют порты через контекст, не зная о сетевом транспорте.

**Результат:**
- Доменные правила независимы от Django, React, Postgres, MongoDB, scikit-learn, Apollo и т.д.
- Реализацию транспортного слоя или способ хранения данных можно менять без изменения бизнес-логики.

---

## 9. ИТОГ

ResumeMatchEDU спроектирован как обучаемый PoC с упором на прозрачную архитектуру:

- Чистая архитектура (core → application → interface/presentation → infrastructure)
- Dependency Inversion и Dependency Injection и на бэкенде, и на фронтенде
- Разделение доменной логики от инфраструктуры (БД, ML, файловое хранилище)
- Монорепозиторий с едиными контрактами
- Простой UI поверх строгих use case'ов

Это позволяет:
- быстро показать рабочий прототип;
- безопасно масштабировать (добавить новые сервисы: ретрейн, отчёты, экспорт);
- менять конкретные технологии (способ вызова API, движок матчинг-алгоритма, тип хранилища).
