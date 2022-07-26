![Django](https://img.shields.io/badge/django%20-%23092E20.svg?&style=for-the-badge&logo=django&logoColor=white)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?&style=for-the-badge&logo=postgresql&logoColor=white)
![Gunicorn](https://img.shields.io/badge/gunicorn-%298729.svg?style=for-the-badge&logo=gunicorn&logoColor=white)
![Nginx](https://img.shields.io/badge/nginx%20-%23009639.svg?&style=for-the-badge&logo=nginx&logoColor=white)
![Docker](https://img.shields.io/badge/docker%20-%230db7ed.svg?&style=for-the-badge&logo=docker&logoColor=white)
![Github](https://img.shields.io/badge/github%20-%23121011.svg?&style=for-the-badge&logo=github&logoColor=white)


![Foodgram project](https://github.com/kirsbrosnone/foodgram-project-react/actions/workflows/foodgram.yml/badge.svg)

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

### Запуск проекта на своем ПК.
`Требуется установленный Docker, docker-compose.`

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
3. Локально перейти в склонированный репозиторий `/infra/`
4. Выполнить запуск docker-compose скрипта:
```sh
docker-compose up -d --build
```
5. После выполнить команды:
```sh
docker-compose exec -T backend python manage.py migrate --noinput
docker-compose exec -T backend python manage.py collectstatic --noinput
docker-compose exec -T backend python manage.py createsuperuser
```
6. Проверить работу сайта

PS. Инструкция по развертыванию проекта на своем сервере находится в `/.github/workflows/`

### Автор

Роман Кирсанов, Студент факультета Бэкенд Яндекс.Практикум. Когорта №9+
