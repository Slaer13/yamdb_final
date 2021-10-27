![example workflow](https://github.com/slaer13/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg?branch=master)

## Подготовка и запуск проекта
### Склонировать репозиторий на локальную машину:
```
git clone https://github.com/Slaer13/yamdb_final.git
```
## Для работы с удаленным сервером (на ubuntu):
### Выполните вход на свой удаленный сервер

### Установите docker на сервер:
```
sudo apt install docker.io 
```
### Установите docker-compose на сервер:
```
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
```
### Локально отредактируйте файл nginx/default.conf и в строке server_name впишите свой IP
### Скопируйте файлы docker-compose.yml и nginx.conf на сервер:
```
scp docker-compose.yml <username>@<host>:/home/<username>/docker-compose.yml
scp nginx.conf <username>@<host>:/home/<username>/nginx.conf
```

### После успешной сборки на сервере выполните команды (только после первого деплоя):
#### Соберите статические файлы:
```
sudo docker-compose exec web python manage.py collectstatic --noinput
```
#### Применитe миграции:
```
sudi docker-compose exec web python manage.py makemigrations
sudo docker-compose exec web python manage.py migrate --noinput
```
#### Загрузите ингридиенты в базу данных (не обязательно)
```
sudo docker-compose exec web python manage.py loaddata fixtures.json
```
#### Создать суперпользователя Django:
```
sudo docker-compose exec web python manage.py createsuperuser
```
### Проект будет доступен по вашему IP
### Для работы с Workflow добавьте в Secrets GitHub переменные окружения для работы:
```
DOCKER_PASSWORD=<пароль от DockerHub>
DOCKER_USERNAME=<имя пользователя>
USER=<username для подключения к серверу>
HOST=<IP сервера>
PASSPHRASE=<пароль для сервера, если он установлен>
SSH_KEY=<ваш SSH ключ (для получения команда: cat ~/.ssh/id_rsa)>
TG_CHAT_ID=<ID чата, в который придет сообщение>
TELEGRAM_TOKEN=<токен вашего бота>
SECRET_KEY=<секретный ключ проекта django>
DB_ENGINE=django.db.backends.postgresql
DB_NAME=<имя базы данных postgres>
DB_USER=<пользователь бд>
DB_PASSWORD=<пароль>
DB_HOST=db
DB_PORT=5432
ALLOWED_HOSTS = <'список разрешённых хостов'> (по умолчнию доступны все, через пробел)
DEBUG = <режим отладки> (0 или 1)
```

## Workflow состоит из трёх шагов:
- Сборка и публикация образа бекенда на DockerHub.
- Автоматический деплой на удаленный сервер.
- Отправка уведомления в телеграм-чат.


##Админка находится по адресу:
```
http://darkertheblack.ru/admin/
```
##API
```
http://darkertheblack.ru/api/v1/
```
##Redoc
```
http://darkertheblack.ru/redoc/
```