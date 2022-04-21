# Сервис уведомлений

Сервис разработан на django rest framework


## Установка и запуск

1. Склонировать репозиторий с Github:

````
git clone git@github.com:Witaly3/notification_service.git
````
2. Перейти в директорию проекта

3. Создать виртуальное окружение:

````
python -m venv venv
````

4. Активировать окружение: 

````
source\venv\bin\activate
````
5. В файле .evn заполнить необходимые данные: ```TOKEN = '<your token>'```
 
6. Установка зависимостей:

```
pip install -r requirements.txt
```

7. Создать и применить миграции в базу данных:
```
python manage.py makemigrations
python manage.py migrate
```
8. Запустить сервер
```
python manage.py runserver
```
9. Запустить celery
```
celery -A notification_service worker -l info
```
10. Запустить flower

```
celery -A notification_service flower --port=5555
```
***
### Запуск тестов
``` 
python manage.py test
```
***