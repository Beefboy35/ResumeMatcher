# Backend (Django + GraphQL + DRF)

Слои:
- core: доменные сущности и порты
- application: use cases
- interface: GraphQL резолверы и DRF views
- infrastructure: реализации портов (ORM, GridFS, tf-idf)
- di: контейнер зависимостей