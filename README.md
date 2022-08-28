![Django](https://img.shields.io/badge/django%20-%23092E20.svg?&style=for-the-badge&logo=django&logoColor=white)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?&style=for-the-badge&logo=postgresql&logoColor=white)
![Gunicorn](https://img.shields.io/badge/gunicorn-%298729.svg?style=for-the-badge&logo=gunicorn&logoColor=white)
![Nginx](https://img.shields.io/badge/nginx%20-%23009639.svg?&style=for-the-badge&logo=nginx&logoColor=white)
![Docker](https://img.shields.io/badge/docker%20-%230db7ed.svg?&style=for-the-badge&logo=docker&logoColor=white)
![Github](https://img.shields.io/badge/github%20-%23121011.svg?&style=for-the-badge&logo=github&logoColor=white)


[![Foodgram project](https://github.com/kirsbrosnone/foodgram-project-react/actions/workflows/foodgram.yml/badge.svg)]

# Foodgram-project-react

### Описание проекта
Сайт Foodgram, «Продуктовый помощник». На этом сервисе пользователи смогут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

# Развернутый проект на сервере YandexCloud:

Backend:

 `84.252.140.50/api/` - api
 
 `84.252.140.50/api/docs/` - документация к api
 
 `84.252.140.50/admin` - админ-интерфейс проекта (login/password: admin/Admin12345!)

Frontend:

 `84.252.140.50` - frontend проекта 

### Создание пользователя администратором
Пользователя может создать администратор — через админ-зону сайта или через POST-запрос на специальный эндпоинт `api/v1/users/` (описание полей запроса для этого случая — в документации). В этот момент письмо с кодом подтверждения пользователю отправлять не нужно.
После этого пользователь должен самостоятельно отправить свой `email` и `username` на эндпоинт `/api/v1/auth/signup/`, в ответ ему должно прийти письмо с кодом подтверждения.
Далее пользователь отправляет POST-запрос с параметрами `username` и `confirmation_code` на эндпоинт `/api/v1/auth/token/`, в ответе на запрос ему приходит `token` (JWT-токен), как и при самостоятельной регистрации.

### Ресурсы API YaMDb
- Ресурс `auth`: аутентификация.
- Ресурс `users`: пользователи.
- Ресурс `titles`: произведения, к которым пишут отзывы (определённый фильм, книга или песенка).
- Ресурс `categories`: категории (типы) произведений («Фильмы», «Книги», «Музыка»).
- Ресурс `genres`: жанры произведений. Одно произведение может быть привязано к нескольким жанрам.
- Ресурс `reviews`: отзывы на произведения. Отзыв привязан к определённому произведению.
- Ресурс `comments`: комментарии к отзывам. Комментарий привязан к определённому отзыву.

### Запуск проекта на собственном сервере через Github Actions.

`Проект проверен на сервере с ОС Ubuntu 22.04 LTS.`
`Для корректной работы, отключите веб-сервер NGINX и настройте Firewall`
`Для корректной работы, отключите все работающие docker-контейнеры`

1. Скопировать или сделать форк репозитория.
2. На странице скопированного проекта, перейти `Github - Settings - Secrets - Action secrets` и добавить следующие значения: 
```sh
SECRET_KEY - секретный ключ приложения django (можно найти в settings проекта).
DB_NAME - имя базы данных (postgres, по умолчанию).
POSTGRES_USER - пользователь базы данных, (postgres, по умолчанию).
POSTGRES_PASSWORD - пароль пользователя, (postgres, по умолчанию).
DB_ENGINE - база данных (django.db.backends.postgresql, по умолчанию).
DB_HOST - хост (db, по умолчанию).
DB_PORT - порт (5432, по умолчанию).
DOCKER_USERNAME - имя пользователя в DockerHub.
DOCKER_PASSWORD - пароль пользователя в DockerHub.
HOST - ip-адрес сервера на который выполняется деплой.
USER - пользователь, который будет логиниться в сервер.
SSH_KEY - приватный ssh-ключ.
PASSPHRASE - кодовая фраза для ssh-ключа.
TELEGRAM_TO - id телеграм-аккаунта (пишем @userinfobot "/start").
TELEGRAM_TOKEN - токен бота (@BotFather, "/token <имя бота>" для выдачи нового token, или "/mybots" для просмотра текущего токена).
```
3. Локально перейти в `/infra/nginx.conf` поменять ip-адрес Server name на свое.
4. Подключиться на свой сервер. Перейти в дирректорию `home/<username>/`.
5. Скопировать с локальной машины на свой сервер файлы: `infra/docker-compose.yaml` и `infra/nginx.conf`. Сделать это можно при помощи команды scp. Например, находясь в директории `/infra/` выполнить команду: `scp default.conf <username>@<host>/home/<username>/nginx.conf`.
6. Если на сервере не установлен Docker и docker-compose, то необходимо выполнить установку:
```sh
sudo apt install docker.io
```
```sh
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
```
```sh
sudo chmod +x /usr/local/bin/docker-compose
```
Проверяем, что установка прошла корректно:
```sh
sudo docker --version # появится сообщение вида Docker version 20.10.12, build 20.10.12-0ubuntu2~20.04.1
```
```sh
sudo docker-compose --version # появится сообзение вида docker-compose version 1.29.2, build 5becea4c
```
7. Запушить все изменения в свой репозиторий на Github. Автоматически запустится workflow.

8. Создать суперпользователя (для логина в админ-зону api), на подключенном сервере:
```sh
sudo docker-compose exec backend python manage.py createsuperuser
```
9. Проверить работу сайта

### Автор

Роман Кирсанов, Студент факультета Бэкенд Яндекс.Практикум. Когорта №9+
