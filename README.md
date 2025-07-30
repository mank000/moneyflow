# Django MoneyFlow App

Приложение для учёта и управления денежными потоками с возможностью фильтрации по типам, категориям, подкатегориям, статусам и датам.

Ссылка на демо верисю: http://217.114.7.215/

Ссылка на админку: http://217.114.7.215/admin/

username: admin

password: admin

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

4. По желанию можно использовать фикстуру для наполнения БД.

```bash
docker compse moneyflow exec python manage.py loaddata initial_data
```

5. Перейти в браузере:

Админка: http://localhost/admin/

Основной интерфейс: http://localhost/

🛠 Стек

Python / Django

SQLite (по умолчанию)

HTML (Django Templates)
