![Nginx](https://img.shields.io/badge/nginx-%23009639.svg?style=for-the-badge&logo=nginx&logoColor=white) ![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E) ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white) ![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray) ![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white) ![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white) ![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white) ![GitHub Actions](https://img.shields.io/badge/github%20actions-%232671E5.svg?style=for-the-badge&logo=githubactions&logoColor=white)
# Foodgram

Сайт доступен: https://emelyanov.myvnc.com/
_________________________________________________
## Описание
Сайт с рецептами, избранными, корзиной, который находится в контейнере.

### YaMDB - возможности:

- Создать рецепт.
- Добавлять другие рецепты в избранное.
- Подписываться на авторов.
- Сохранять рецепты в список покупок для его печати.
- Дополнительно проект обладает удобным API-интерфейсом
 
_____________________________________________________

## Техническое описание

### Примененные технологии
 > Django==3.2 
 > djangorestframework==3.12.4 
 > djoser==2.1.0 
 > django-filter==22.1 
 > gunicorn==20.0.4 
 > psycopg2-binary==2.9.5 
 > pytz==2020.1 
 > sqlparse==0.3.1 
 > python-dotenv==0.21.0 
 > Pillow==9.5.0

### Ресурсы API foodgram (основные):
- Ресурс auth: аутентификация.
/api/auth/token/login/ /api/auth/token/logout/ - (POST) получение/удаление токена
- Ресурс users: пользователи. /api/users/{id} - (GET) персональная страница пользователя
- Ресурс tags: теги. /api/tags/ - (GET) получение списка всех тегов
- Ресурс ingredients: ингридиенты. /api/ingredients/ - (GET) получение списка всех ингредиентов
- Ресурс recipes: рецепты. /api/recipes/ - (GET) получение списка всех рецептов

### Как локально запустить проект:
!!!Запустить на локальной машине Docker!!!


Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:emelyanov-sergey/foodgram-project-react.git
```

```
cd infra
```

Создать файл .env:
```
touch .env
```
Открыть в редакторе файл .env:
```
nano .env
```
Погрузить в файл .env следующие значения:
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres # установите свой пароль для подключения к базе
DB_HOST=db
DB_PORT=5432
SECRET_KEY='...' # секретный ключ, нужно установить свой
```
Закрыть файл .env с сохранием:
```
^X
```
Чтобы оставить имя без изменения нажмите enter (return для MacOS), далее
выходим в корневую директорию:
```
cd ..
```
Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

```
source venv/bin/activate
```
Переход в директорию infra и запуск:
```
cd infra
```
```
docker-compose up
```
Необходимо открыть новый терминал и ввести по порядку следующие команды:
```
docker-compose exec web python manage.py makemigrations
```
```
docker-compose exec web python manage.py migrate
```

```
docker-compose exec web python manage.py collectstatic --no-input
```
Создайте суперюзера:
```
docker-compose exec web python manage.py createsuperuser
```
Наполнить базу данных ингридлиентами и тегами:
```
docker-compose exec web python manage.py basefill
```
```
docker-compose exec web python manage.py tagfill
```

Документация к APi доступна по адресу: 
```
http://localhost/redoc/
```

## Запуск проекта на боевом сервере

Устанавливаем на сервер docker и docker-compose

Копируем на сервер файлы docker-compose.yaml и default.conf

Переходим в директорию infra и вводим команду:
```
scp docker-compose.yaml <логин_на_сервере>@<IP_сервера>:/home/<логин_на_сервере>/docker-compose.yaml
```
далее вводим следующие команды:
```
cd nginx
scp default.conf <логин_на_сервере>@<IP_сервера>:/home/<логин_на_сервере>/nginx/default.conf
```
В Secrets на Github необходимо добавить следующие переменные:
```
DB_ENGINE=django.db.backends.postgresql # указать, что проект работает с postgresql
DB_NAME=postgres # имя базы данных
POSTGRES_USER=postgres # логин для подключения к базе данных
POSTGRES_PASSWORD=postgres # пароль для подключения к БД
DB_HOST=db # название сервиса БД (контейнера) 
DB_PORT=5432 # порт для подключения к БД
DOCKER_USERNAME= # Username на DockerHub
DOCKER_PASSWORD= # Пароль на DockerHub
HOST= # ip боевого сервера
USER= # Имя пользователя на удалённом сервере
SSH_KEY= # SSH-key компьютера (локальный ключ), с которого будет происходить подключение к удалённому серверу
PASSPHRASE= #Если для ssh используется фраза-пароль
TELEGRAM_TO= #ID пользователя в Telegram, можно узнать у @userinfobot
TELEGRAM_TOKEN= #ID бота в Telegram подскажет @BotFather
```

После успешного пуша и в случае, если все переменные указаны верно проект запустится на сервере.

Далее в терминале, подключенном к боевому серверу вводим поочередно следующие команды:
```
sudo docker-compose exec web python manage.py makemigrations
```
```
sudo docker-compose exec web python manage.py migrate
```
```
sudo docker-compose exec web python manage.py collectstatic --no-input
```
```
sudo docker-compose exec web python manage.py createsuperuser
```
```
sudo docker-compose exec web python manage.py basefill
```
```
sudo docker-compose exec web python manage.py tagfill
```
Проект зарущен, с помощью супрюзера можно подключаться

## Примеры запросов
### Регистрация пользователя
>Тип запроса 
```POST```
>Endpoint 
```/api/users/```

Запрос:
```
{
    "email": "user@yandex.ru",
    "username": "IvanEX",
    "first_name": "Ivan",
    "last_name": "Ivanov",
    "password": "Qwerty1234"
}
```
Ответ:
```
{
    "email": "user@yandex.ru",
    "id": 2,
    "username": "IvanEX",
    "first_name": "Ivan",
    "last_name": "Ivanov",
}
```
______________________________________
### Автор
Емельянов Сергей(https://github.com/emelyanov-sergey)
