# Django MoneyFlow App

Приложение для учёта и управления денежными потоками с возможностью фильтрации по типам, категориям, подкатегориям, статусам и датам.
Для работы настроен фронтенд и админка.
## Установка

1. Клонировать репозиторий:

```bash
git clone
cd moneyflow
```

2. Заполнить .env файл в папке с проектом по примеру в файле .env.example

3. Запустить docker-compose

```bash
docker compose up -d
```

4. По желанию использовать фикстуру для наполнения БД.

```bash
docker compose -f docker-compose.yml exec moneyflow python manage.py loaddata initial_data.json
```

5. Создать суперпользователя

```bash
docker compose -f docker-compose.yml exec moneyflow python manage.py createsuperuser
```

6. Перейти в браузере:

Админка: http://localhost:8000/admin/

Основной интерфейс: http://localhost:8000/

## Стек

Python / Django

SQLite (по умолчанию)

HTML (Django Templates)

Bootstrap
