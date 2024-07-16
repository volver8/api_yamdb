# Api_yamdb

## Описание проекта.
*В данном проекте будет реализоваться возможность создания произведений пользователями с разными права доступа.*
*Также можно выбрать критерии произведения, создать на них обзоры с комментариями.*

## Документация проекта.
*Адрес документации проекта:* [http://127.0.0.1:8000/redoc/](http://127.0.0.1:8000/redoc/)

![](https://www.ibexa.co/var/site/storage/images/_aliases/ibexa_content_full/3/4/1/0/300143-1-eng-GB/d4255a27c1fa-AdobeStock_261705271_What-is-an-API.jpeg)

## Алгоритм запуска проекта.
*Адрес репозитория:*
```
https://github.com/volver8/api_yamdb
```
*Клонировать репозиторий по SSH-ключу:*
```
git clone 'SSH_ключ_проекта'
```
*Перейти в папку проекта: api_yamdb.*
*Развернуть виртуальное окружени:*
```
python -m venv venv
```
*Активировать виртуальное окружение:*
```
source venv/Scripts/activate
```
*Установка зависимостей из файла requirements.txt:*
```
pip install -r requirements.txt
```
*Выполнить миграции:*
```
python manage.py migrate
```
*Перейти в папку api_yamdb:*
```
cd api_yamdb
```
*Запустить сервер*
```
python manage.py runserver 
```

## Импорт данных из csv.
```
python manage.py load_csv
```
## Примеры запросов.
There are some examples of requests:
  -  Model Title

      - GET request: /api/v1/titles/
          ```
          {
            "count": 0,
            "next": "string",
            "previous": "string",
            "results": [
              {
                "id": 0,
                "name": "string",
                "year": 0,
                "rating": 0,
                "description": "string",
                "genre": [
                  {
                  "name": "string",
                  "slug": "^-$"
                  }
                ],
                "category": {
                  "name": "string",
                  "slug": "^-$"
                }
              }
            ]
          }
          ```
       
  -  JWT token

      - POST request: /api/v1/auth/token/

        - Request samples
        ```
        {
          "username": "^w\\Z",
          "confirmation_code": "string"
        }
        ```
        - Response samples
        ```
        {
          "token": "string"
        }
        ```

## Разработчики:

- Vladimir Rusakov: https://github.com/volver8
- Evgeny Kudryashov: https://github.com/GagarinRu
- Evgeny Cherednichenko: https://github.com/Moreggg
