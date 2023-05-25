# Foodgram

## Description
## Docker
## DB
## Commands
## DB import
## Information and Access
## Creator

---
## Description

The Foodgram project:
  - Create and manage recipes
  - View recipes of users
  - Add recipes of users in Favorites and Cart
  - Subscribe to other users
  - Download the list of ingredients for the recipes

---
## Docker

Containers: db, frontend, backend, nginx   
Docker and Docker Compose need to be installed 

---
## DB

Database: PostgreSQL 

.env:
```python
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
```

---
## Commands

GIT Clone:
```bash
SSH: git clone git@github.com:zakharovvladimir/foodgram-project-react.git
```

requirements.txt install:
```bash
python3 -m pip install --upgrade pip
```
```bash
pip install -r requirements.txt
```

./infra/:
```bash
docker-compose up -d --build
```

DB migrations:
```bash
docker-compose exec backend python manage.py migrate
```

Superuser:
```bash
docker-compose exec backend python manage.py createsuperuser
```

Static:
```bash
docker-compose exec backend python manage.py collectstatic --no-input
```

---
## DB import

Ingredients import:
```bash
docker-compose exec backend python manage.py import
```

---
## Information and Access

Technology Stack: Python 3.9, Django, Django Rest Framework, PostgreSQL, React, Docker, nginx, gunicorn, Djoser 
```bash
Access:  51.250.103.14 // Administrator: vladimirzakharov / MyAdminPass // User: vladimir.zakharov.s@yandex.ru / MyUserPass
```
---
## Creator

Vladimir Zakharov 
vladimir.zakharov.s@yandex.ru 
