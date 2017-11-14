URL shortener
======

RESTful API для сокращателя ссылок

Стек: python(Flask) + PostgreSQL + ngnix

Установка
-----

Перед тем, как приступить к запуску, убедитесь, что у вас установлены **docker** и **docker-compose**

Для того, чтобы развернуть приложение, в корневой директории проекта выполните:

    docker-compose up -d

*При первом запуске, сборка может занять длительное время*

После сборки, приложение будет запущено локально: <http://0.0.0.0:8080>


Описание
------
#### Авторизация
Для авторизации исользуется HTTP Basic Authorization
Запросы к сервису осуществляются посредством методов GET (+ GET-параметры) и  POST, DELETE (+ JSON)
Сервис возвращает данные в формате JSON

Ресурсы и методы API
------

#### /api/v1/users 
**Ресурс**, предоставляющий работу с пользователями.
- POST /api/v1/users - регистрация пользователя (авторизация не требуется).
    
    Пример ответа сервера, при успешном выполнении запроса:
        
        {
            "message": "User successfully registered"
        }
    
- GET  /api/v1/users/me - получение информации о текущем авторизованном пользователе.
    
    Пример ответа сервера, при успешном выполнении запроса:
        
        {
            "data": {
                "id": 1,
                "login": "admin",
                "links_created": 2
            }
        }


#### /api/v1/users/me/shorten_urls
**Ресурс**, предоставляющий работу с короткими ссылками пользователя
- POST /api/v1/users/me/shorten_urls - создание новой короткой ссылки
    
    Пример ответа сервера, при успешном выполнении запроса:
        
         {
            "data": {
                "id": 3,
                "url": "http://google.com",
                "short_url": "http://localhost:8080/api/v1/shorten_urls/6506076198b0"
            }
        }

- GET /api/v1/users/me/shorten_urls - получение всех созданных коротких ссылок пользователя

    Пример ответа сервера, при успешном выполнении запроса:
        
         {
            "data": [
                {
                    "id": 1,
                    "url": "http://vk.com",
                    "shortLink": "http://localhost:8080/api/v1/shorten_urls/0b888ec03aed"
                },
                {
                    "id": 2,
                    "url": "http://vk.ru",
                    "shortLink": "http://localhost:8080/api/v1/shorten_urls/897c0286e8ae"
                },
                {
                    "id": 3,
                    "url": "http://google.com",
                    "shortLink": "http://localhost:8080/api/v1/shorten_urls/6506076198b0"
                }
            ]
        }

- GET /api/v1/users/me/shorten_urls/{id} - получение информации о конкретной короткой ссылке пользователя

    Пример ответа сервера при успешном выполнении запроса:

        {
            "data": {
                "id": 1,
                "url": "http://vk.com",
                "short_url": "http://localhost:8080/api/v1/shorten_urls/0b888ec03aed",
                "count_of_redirects": 7,
                "created": "14.11.2017 15:10"
            }
        }

- DELETE /api/v1/users/me/shorten_urls/{id}- удаление короткой ссылки пользователя

    Пример ответа сервера при успешном выполнении запроса:
    
        {
            "message": "Link was successfully deleted""
        }

**Отчеты**

- GET /api/v1/users/me/shorten_urls/{id}/[days,hours,min]?from_date=0000-00-00&to_date=0000-00-00 - получение временного графика количества переходов с группировкой по дням, часам, минутам.

    Полученный ответ представляет собой массив точек с координатами {*x*:*y*}, где *x* - время, *y* - количество переходов
    
    Пример ответа сервера при успешном выполнении запроса:
    
       {
            "data": {
                "14.11.2017 00:00": 7,
                "14.11.2017 01:00": 0,
                "14.11.2017 02:00": 0,
                "14.11.2017 03:00": 0,
                "14.11.2017 04:00": 0,
                "14.11.2017 05:00": 2,
                "14.11.2017 06:00": 0,
                "14.11.2017 07:00": 0,
                "14.11.2017 08:00": 1,
                "14.11.2017 09:00": 0,
                "14.11.2017 10:00": 5,
                "14.11.2017 11:00": 0,
                "14.11.2017 12:00": 3,
                "14.11.2017 13:00": 0,
                "14.11.2017 14:00": 0,
                "14.11.2017 15:00": 5,
                "14.11.2017 16:00": 2,
                "14.11.2017 17:00": 0,
                "14.11.2017 18:00": 0,
                "14.11.2017 19:00": 11,
                "14.11.2017 20:00": 9,
                "14.11.2017 21:00": 0,
                "14.11.2017 22:00": 0
            }
        }

- GET /api/v1/users/me/shorten_urls/{id}/referers - получение топа из 20 сайтов - иcточников переходов*
    
    *-источник перехода (HTTP referrer) - один из заголовков HTTP запроса, который содержит информацию о сайте, с которого пользователь перешел по ссылке.
В некоторых случаях не может быть определен, и сокращатель ссылок записывает в базу переход со значением поля *referrer* = None.

    
    Пример ответа сервера при успешном выполнении запроса: 
    
        {
            "data": [
                {
                    "referrer": "None",
                    "count_of_redirects": 7
                },
                {
                    "referrer": "http://vk.com",
                    "count_of_redirects": 2
                }
            ]
        }
    

#### /api/v1/shorten_urls
Ресурс, предоставляющий работу с короткими ссылками (авторизация не требуется)
GET /api/v1/shorten_urls/{hash} - переход по ссылке (302 rediret)



## some notes while developing:

=========== Header basic auth ===========

    token_str = base64encoded "login:password"
    curl -H "Authorization: token_str"

======= User:passwd basic auth ==========

    curl http://localhost:8080/api/v1/users -i -u admin:qwerty
        
=========== curl add new user ===========

    curl http://localhost:8080/api/v1/users -i -H "Content-Type: application/json" -X POST -d '{"login":"your_login","password":"yourqwerty"}'

=========== curl add new url  ===========

    curl http://localhost:8080/api/v1/users/me/shorten_urls -i -H "Content-Type: application/json" -X POST -d '{"url":"http://promedia-perm.ru"}' -u admin:123