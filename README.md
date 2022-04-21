# Сервис уведомлений

Сервис разработан на django rest framework


## Установка и запуск

1. Склонировать репозиторий с Github:

````
git clone git@github.com:AleksSpace/Message_manager.git
````
2. Перейти в директорию проекта

3. Создать виртуальное окружение:

````
python -m venv venv
````

4. Активировать окружение: 

````
. \venv\Scripts\activate
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

***
### Запуск тестов
``` 
python manage.py test
```
***
### URLS

```http://0.0.0.0:8000/api/``` - api проекта

```http://0.0.0.0:8000/api/clients/``` - клиенты

```http://0.0.0.0:8000/api/mailings/``` - рассылки

```http://0.0.0.0:8000/api/mailings/fullinfo/``` - общая статистика по всем рассылкам

```http://0.0.0.0:8000/api/mailings/<pk>/info/``` - детальная статистика по конкретной рассылке

```http://0.0.0.0:8000/api/messages/``` - сообщения

```http://0.0.0.0:8000/docs/``` - docs проекта(swagger)

```http://0.0.0.0:8000/redoc/``` - docs проекта(redoc)