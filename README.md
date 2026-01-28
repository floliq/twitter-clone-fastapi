# 🏷️ Twitter Clone Backend FastAPI

## Основные возможности:
- Добавление постов с медиа
- Просмотр твитов
- Подписки и отписки между пользователями
- Лайки и снятие лайков
- Просмотр профиля пользователя

## Структура проекта
- main.py - Точка входа в приложение
- app/media/** - Медиа-файлы
- app/models/** - ORM-модели
- app/repositories/** - Репозитории (логика по работе с БД)
- app/routes/** - Маршруты(эндпоинты)
- app/schemas/** - Pydantic-схемы
- app/services/** - Сервисы (бизнес-логика)
- app/app.py - Инициализация проекта
- app/app.py - Настройки проекта
- app/db.py - Логика БД
- app/depends.py - Зависимости (Dependency injections)
- app/exception_handlers.py - Обработчики ошибок
- frontend/** - Frontend
- migrations/** - Миграции БД
- tests/** - Тесты приложения

## 🚀 Запуск через Docker

### 1. Клонирование репозитория
```bash
git https://github.com/floliq/twitter-clone-fastapi.git
cd twitter-clone-fastapi
```

### 2. Запуск docker-compose
```bash
docker-compose up -d
```

## 🚀 Запуск для локальной разработки

### 1. Клонирование репозитория
```bash
git https://github.com/floliq/twitter-clone-fastapi.git
cd twitter-clone-fastapi
```

### 2. Создание и активация виртуального окружения
Рекомендуемая версия: ***Python 3.13.2***
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Установка зависимостей
```bash
pip install -r requirements.tsx
```

### 3. Создание файла .env и заполнение (ВАЖНО ОТКРЫТЬ .env.example)
```
POSTGRES_URL=АДРЕС_БД #localhost:5432
POSTGRES_DB=ИМЯ_БД
POSTGRES_USER=ИМЯ_ПОЛЬЗОВАТЕЛЯ
POSTGRES_PASSWORD=ПАРОЛЬ
```

### 4. Создание локальной базы данных
```
psql -U postgres
CREATE USER ИМЯ_ПОЛЬЗОВАТЕЛЯ WITH PASSWORD 'ПАРОЛЬ';
CREATE DATABASE ИМЯ_БД OWNER ИМЯ_ПОЛЬЗОВАТЕЛЯ;
GRANT ALL PRIVILEGES ON DATABASE ИМЯ_БД TO ИМЯ_ПОЛЬЗОВАТЕЛЯ;
```

### 5. Обновить миграции базы данных
```
alembic upgrade head
```

### 6. Запуск приложения
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 7. Установка nginx
```bash
apt install nginx
```

### 8. Настройка конфига /nginx/local
```
server {
        listen 80;

        # Укажите папку до фронтенда
        root /home/floliq/skillbox/Diploma/frontend;
        index index.html;


        location /api/ {
                proxy_pass http://127.0.0.1:8000;
                include proxy_params;
        }

        location /docs/ {
                proxy_pass http://127.0.0.1:8000/docs;
                include proxy_params;
        }



        location /media/ {
                # Укажите папку до папки media
                alias /home/floliq/skillbox/Diploma/app/media/;
                expires 1y;
                access_log off;
        }

        location / {
                try_files $uri $uri/ /index.html;
        }
}
```

После этого API доступно по адресу: [http://localhost](http://localhost:8000)
Swagger: [http://localhost/docs/](http://localhost:8000/docs)
