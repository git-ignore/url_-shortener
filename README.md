## URL shortener 

RESTful API 

python(Flask) + PostgreSQL + ngnix

## some notes while developing:

=========== Header basic auth ===========

    token_str = base64encoded "login:password"
    curl -H "Authorization: token_str"

======= User:passwd basic auth ==========

    curl http://localhost:8080/api/v1/users -i -u admin:qwerty
        
=========== curl add new user ===========

    curl http://localhost:8080/api/v1/users -i -H "Content-Type: application/json" -X POST -d 
    '{"login":"your_login","password":"yourqwerty"}'

=========== curl add new url  ===========

    curl http://localhost:8080/api/v1/users/me/shorten_urls -i -H "Content-Type: application/json" -X POST -d '{"url":"http://promedia-perm.ru"}' -u admin:123