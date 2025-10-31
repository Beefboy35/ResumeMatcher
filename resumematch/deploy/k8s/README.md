# ResumeMatcher — локальный деплой в Minikube

Эти манифесты разворачивают API, Frontend, Postgres и MongoDB в локальном кластере Minikube.

## Предварительно

- Контекст `kubectl` указывает на `minikube`.
- Образы собраны локально и загружены в Minikube.
- Секреты заполнены (см. `secret.example.yaml`).

## Шаги

1) Создать namespace и конфиги/секреты:

```powershell
kubectl apply -f resumematch/deploy/k8s/namespace.yaml
kubectl apply -f resumematch/deploy/k8s/config.yaml
kubectl apply -f resumematch/deploy/k8s/secret.example.yaml
```

2) Собрать и загрузить образы в Minikube:

```powershell
docker build -t resumematch/api:local -f resumematch\deploy\Dockerfile.api .
docker build -t resumematch/frontend:local -f resumematch\deploy\Dockerfile.frontend .
minikube image load resumematch/api:local
minikube image load resumematch/frontend:local
```

3) Развернуть базы данных:

```powershell
kubectl apply -f resumematch/deploy/k8s/postgres.yaml
kubectl apply -f resumematch/deploy/k8s/mongodb.yaml
```

Проверить готовность:

```powershell
kubectl -n resumematch get pods
kubectl -n resumematch logs statefulset/postgres
kubectl -n resumematch logs statefulset/mongodb
```

4) Развернуть API и Frontend:

```powershell
kubectl apply -f resumematch/deploy/k8s/api.yaml
kubectl apply -f resumematch/deploy/k8s/frontend.yaml
kubectl -n resumematch get deploy,svc,pods
```

5) Доступ локально (без домена/ingress):

```powershell
kubectl -n resumematch port-forward svc/api 8000:8000
# В новом окне:
kubectl -n resumematch port-forward svc/frontend 5173:5173
```

Теперь:

- API: http://localhost:8000/
- Swagger: http://localhost:8000/api/docs/
- Redoc: http://localhost:8000/api/redoc/
- Frontend (Vite dev): http://localhost:5173/

## Примечания

- Файл `secret.example.yaml` содержит шаблон; при использовании в реальной среде замените значения и переименуйте в `secret.yaml`.
- Если хотите Ingress (локально, без публичного домена):
  - `minikube addons enable ingress`
  - создайте Ingress манифест и добавьте запись в `hosts` (например, `127.0.0.1 resumematch.local`).
- Для прод-стиля фронтенда используйте образ со сборкой статики и Nginx; текущий манифест запускает Vite dev‑сервер для скорости.