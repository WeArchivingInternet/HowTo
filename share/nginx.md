# Nginx

[Официальный сайт](https://nginx.org/)

Nginx (Engine-X) - высокопроизводительный web сервер. Для сохранения интернета он интересен своим модулем - [autoindex](https://nginx.org/ru/docs/http/ngx_http_autoindex_module.html), который позволяет выводить содержимое каталога и скачивать из него файлы. Собственно это как раз по теме раздачи файлов.

# Предупреждение

Раздача файлов в анонимных сетях может быть не безопасна. 

__ВАША БЕЗОПАСНОСТЬ - ВАША ЗАБОТА__. 

Поэтому старайтесь придерживаться следующих правил:

- __ВКЛЮЧИТЕ ФАЙРВОЛЛ__ ([тык](https://github.com/WeArchivingInternet/HowTo/blob/main/share/yggdrasil.md#%D0%BE%D0%B1%D1%8F%D0%B7%D0%B0%D1%82%D0%B5%D0%BB%D1%8C%D0%BD%D0%B0%D1%8F-%D0%BD%D0%B0%D1%81%D1%82%D1%80%D0%BE%D0%B9%D0%BA%D0%B0))
- __ОБНОВЛЯЙТЕСЬ__
- __Не забывайте выставлять правильные права на файлы__
- __Разворачивайте сервера в контейнерах или виртуальных машинах__

## Установка и настройка (Linux)

Рассмотрим установку и настройку на примере дистрибутива `Debian`

Пакет доступен в стандартном репозитории Debian, поэтому достаточно выполнить:

```sh
apt update; apt upgrade; apt install nginx -y; systemctl status nginx
```

Убедившись, что сервер запустился, можно приступать к его конфигурированию. 

## Конфигурация

Конфигурационные файлы находятся в каталоге `/etc/nginx`. Но перед созданием нового файла нужно очистить от начальной конфигурации

```sh
cd /etc/nginx/sites-enabled && rm -f *
```
Также, желательно, создать отдельный каталог для хранения файлов под раздачу. В примере мы будем использовать каталог `/var/www/share`

```sh
# Создаем каталог
mkdir /var/www/share
```

Далее вооружаемся любимым текстовым редактором и идем создавать новую конфигурацию. Для этого достаточно создать файл с любым именем по пути `/etc/nginx/sites-avaliable`. Для примера назовем его `share`. После создания прописываем туда следующие строки:

```nginx
server {
        listen 80;
        listen [::]:80;
        root /var/www/share;
        location / {
                try_files $uri $uri/ =404;
        }

        autoindex on;
        autoindex_exact_size off;

        server_tokens off;
}
```

Далее выходим из редактора и делаем символьную ссылку указывая nginx, что этот сайт должен быть активен

```sh
ln -s /etc/nginx/sites-available/share /etc/nginx/sites-enabled/
```

Вот теперь можно перезапускать nginx и заходить через браузер на сервер

```sh
systemctl restart nginx
```

Должно получится что-то такое

![blank-nginx](images/nginx-blank-index.png)

Теперь в каталог `/var/www/share` можно загружать файлы и они будут отображаться на первой странице

![list-files](images/nginx-file-list.png)

__Обязательно__ нужно выставить права на каталоги (`0755`) и файлы (`0644`):

```sh
chmod 0755 /var/www/share && chmod 0644 /var/www/share/*
```

## Объяснение каждой строки config'а

```nginx
server {
        listen 80; ## Слушать все адреса IPv4 на порту 80
        listen [::]:80; ## Слушать все адреса IPv6 на порту 80
        root /var/www/share; ## Корневая директория
        location / {                        ## Начиная с корня:
                try_files $uri $uri/ =404;  ## Если файла нет - выкидывать 404
        }

        autoindex on; ## Индексирование файлов включено
        autoindex_exact_size off; ## Отображение размера в байтах выключено

        server_tokens off; ## Отключено отображение версии nginx на служебных страницах
}
```

## Кастомизация

По умолчанию интерфейс листинга очень простой, но его можно изменить за счет модуля [ngx_http_xslt_module](https://nginx.org/ru/docs/http/ngx_http_xslt_module.html), который позволяет преобразовывать XML страницы по заданному шаблону.

Для начала создадим директорию для этих шаблонов и перейдем в неё:

```sh
mkdir /var/www/xslt && cd /var/www/xslt
```

Далее необходимо скачать шаблон. Их можно найти в интернете. Для примера можно взять вот [этот](https://gist.github.com/wilhelmy/5a59b8eea26974a468c9) шаблон. Скачать его можно с помощью `wget`

```sh
wget https://gist.githubusercontent.com/wilhelmy/5a59b8eea26974a468c9/raw/00c657fec00da06c14f92a58f4ecffa123a41ae4/dirlist.xslt
```

После успешной загрузки перейдем к настройке конфигурационного файла. Из предыдушего примера можно вспомнить, что конфигурационный файл у нас находится по пути `/etc/nginx/sites-available/share`, поэтому открываем его с помощью любимого редактора и записываем следующее:

```nginx
server {
        listen 80;
        listen [::]:80;
        root /var/www/share;
        location / {
                try_files $uri @autoindex;
        }

        location @autoindex{
                autoindex on;
                autoindex_exact_size off;

                autoindex_format xml;
                xslt_stylesheet /var/www/xslt/dirlist.xslt;
                xslt_string_param path $uri;
        }

        server_tokens off;
}
```

Перезапускаем сервер и смотрим на результат

```sh
systemctl restart nginx
```

![xslt](images/nginx-xslt-listing.png)

## Ссылки на xslt конфигурации

Помните, что xslt файлы могут загружать дополнительные стили, шрифты, иконки, __JS СКРИПТЫ__ обращаясь за файлами на внешние сервера.

__ЭТО МОЖЕТ БЫТЬ ОПАСНО__

Всегда проверяйте содержимое xslt файлов перед тем, как добавить их на сайт. Не добавляйте их бездумно 

### Список

- [wilhelmy/dirlist.xslt](https://gist.github.com/wilhelmy/5a59b8eea26974a468c9)
- [jbox-web/nginx-index-template](https://github.com/jbox-web/nginx-index-template)
- [abdus/nginx-pretty-index](https://github.com/abdus/nginx-pretty-index/)