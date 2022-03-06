# Запуск зеркала
Коллекция приложений и файлов F-Droid запускается на серверах, управляемых основными участниками F-Droid. Первоначально этот основной репозиторий размещался только на f-droid.org, но по мере роста F-Droid один [f-droid.org](f-droid.org) не справлялся с нагрузкой. F-Droid теперь поддерживает «зеркальные» серверы, которые реплицируют полную копию репозиториев. Размещение зеркала предполагает запуск веб-сервера HTTPS с полной копией репозитория, синхронизированной с помощью `rsync`.

#### Требования
Есть два официальных раздела репозитория F-Droid: «repo» и «archive». Наиболее важно отразить «repo», так как он используется гораздо чаще, чем «archive».

Основными ресурсами, необходимыми зеркалу, являются дисковое пространство и пропускная способность загрузки. Требования к полосе пропускания уменьшаются с каждым новым зеркалом, но требования к диску растут с [разумной скоростью](https://ftp.fau.de/cgi-bin/show-ftp-stats.cgi?statstype=2&what=mirrorsize&mirrorname=fdroid&timespan=-1&graphsize=large&submit=Go%21). На момент написания статьи (март 2019 г.) для основного репозитория требуется чуть более 60 ГБ дискового пространства для файлов размером 24 КБ, а для архива требуется 300 ГБ дискового пространства для файлов размером 52 КБ. Требуемый объем дискового пространства растет с каждым новым выпуском приложения.

Есть много зеркальных серверов, которые предлагают соединение rsync, обязательно выберите зеркало, ближайшее к вашему зеркальному серверу:

* Материковый Китай
	* `rsync -axv mirrors.tuna.tsinghua.edu.cn::fdroid`
* Германия
	* `rsync -axv ftp.fau.de::fdroid`
* Индиана, США
	* `rsync -axv plug-mirror.rcac.purdue.edu::fdroid`
* Швеция
	* `rsync -axv ftp.lysator.liu.se::fdroid`
* Тайвань
	* `rsync -axv mirror.ossplanet.net::fdroid`
* Украина
	* `rsync -axv fdroid.astra.in.ua::fdroid`

Вы можете найти текущую информацию о требованиях к дисковому пространству, запустив в терминале следующее:

```
$ rsync -v --list-only ftp.fau.de::fdroid
```

#### Установка
В этом руководстве предполагается использование Nginx на дистрибутивах, основанные на Debian и зеркалирование основного репозитория и архива. Внесите соответствующие изменения, если вы используете альтернативы или не собираетесь зеркалировать архив. Также замените примеры путей и доменов на свои собственные.

Чтобы получить помощь, не стесняйтесь [обращаться к нам](https://github.com/WeArchivingInternet/HowTo#%D0%B0%D1%80%D1%85%D0%B8%D0%B2%D0%B8%D1%80%D1%83%D0%B5%D0%BC-%D0%B8%D0%BD%D1%82%D0%B5%D1%80%D0%BD%D0%B5%D1%82).

1. Создайте соответствующие каталоги
    ```
    $ sudo mkdir -p /var/www/fdroid/fdroid/repo
    $ sudo mkdir -p /var/www/fdroid/fdroid/archive
    $ sudo chown -R www-data.www-data /var/www/fdroid
    ```
2. Синхронизируйте репозитории. Эти команды лучше всего запускать в терминальном мультиплексоре (`screen`, `tmux` и т. д.), так как их выполнение займет некоторое время. С аргументом `--info=progress2` вы сможете увидеть прогресс.
    ```
    $ sudo -u www-data -E /usr/bin/rsync -aHS  --delete --delete-delay --info=progress2 ftp.fau.de::fdroid/repo/ /var/www/fdroid/fdroid/repo/
    $ sudo -u www-data -E /usr/bin/rsync -aHS  --delete --delete-delay --info=progress2 ftp.fau.de::fdroid/archive/ /var/www/fdroid/fdroid/archive/
    ```
3. Установите cronjob, чтобы поддерживать репозитории в актуальном состоянии.
    Создайте файл cronjob в `/etc/cron.d`
    ```
    $ vi /etc/cron.d/fdroid
    ```
    Заполните файл записями ниже для обновления репозиториев. Эти команды будут запускаться на 35-й минуте каждого 6-го часа. Вы можете изменить это в соответствии с вашими потребностями.
    ```
    35 */6 * * * www-data /usr/bin/rsync -aHS  --delete --delete-delay ftp.fau.de::fdroid/repo/ /var/www/fdroid/fdroid/repo/
    35 */6 * * * www-data /usr/bin/rsync -aHS  --delete --delete-delay ftp.fau.de::fdroid/archive/ /var/www/fdroid/fdroid/archive/
    ```
4. Настройте свой веб-сервер

    Это пример блока сервера для nginx. Если он используется, его следует скопировать в */etc/nginx/sites-available/* и сделать символическую ссылку на */etc/nginx/sites-enabled.* Обратите внимание, что важно, чтобы ваш URI был `/fdroid/repo`, чтобы приложение могло автоматически добавить ваше зеркало.
    ```
    server {
      listen [::]:80 ipv6only=off;

      server_name fdroidmirror.example;

      rewrite ^ https://fdroidmirror.example$request_uri permanent;
    }

    server {
      listen [::]:443 ssl http2 ipv6only=off;

      server_name fdroidmirror.example;

      root /var/www/fdroid/;

      # TODO: https://gitlab.com/snippets/1834032
      location /health {
        proxy_pass http://127.0.0.1:8000/;
      }

      ssl_certificate /etc/letsencrypt/live/fdroidmirror.example/fullchain.pem;
      ssl_certificate_key /etc/letsencrypt/live/fdroidmirror.example/privkey.pem;

      # Вставьте сюда конфигурацию TLS из генератора конфигурации SSL Mozilla https://mozilla.github.io/server-side-tls/ssl-config-generator/
    }
    ```
5. Отправьте свое зеркало для включения
    * Форкните [репозиторий монитора зеркала](https://gitlab.com/fdroid/mirror-monitor), добавьте свое зеркало в README и откройте запрос на слияние (merge request).
    * Откройте вопрос (issue) в [репозитории администратора](https://gitlab.com/fdroid/admin), включая любую соответствующую информацию, с запросом на включение вашего зеркала.
    * Как только основная команда участников сочтет ваше зеркало заслуживающим доверия и надежным, оно будет принято в официальный список.

Кроме того, было бы неплохо включить политику конфиденциальности, чтобы пользователи могли понять, что происходит с их метаданными при использовании зеркала. Purdue PLUG https://plug-mirror.rcac.purdue.edu/info.html и FAU https://ftp.fau.de/datenschutz являются двумя примерами.

#### Также рассмотрите
* Настройте политику конфиденциальности, описывающую, что происходит с метаданными (например, [FAU](https://ftp.fau.de/datenschutz/), [PLUG](https://plug-mirror.rcac.purdue.edu/info.html), [Lysator](https://ftp.lysator.liu.se/datahanteringspolicy.txt)).
* Отправка электронных письем от сбоев cronjob, чтобы вы знали, что синхронизация не удалась.
* Настройте мониторинг на своем зеркале, чтобы знать, выйдет ли оно из строя (в идеале ключевое слово на /srv/mymirror.org/htdocs/fdroid/repo/index-v1.jar)
* Улучшите конфигурацию вашего SSH-сервера (отключите аутентификацию по паролю, установите `fail2ban`)
* Включить автоматические обновления безопасности (в Debian `apt install unattended-upgrades`)

## Запуск основного зеркала (получение синхронизации через push)

Предпочтительной настройкой является отправка обновлений F-Droid на основное зеркало через *rsync* через *ssh* с аутентификацией по ключу SSH. Это то же самое, что и [Debian](https://www.debian.org/mirror/push_server#sshtrigger), ключевое отличие состоит в том, что в настоящее время не используется скрипт для `command=""`, а вместо этого есть жестко запрограммированная команда rsync. Это отлично ограничивает взаимодействие безопасности только для того, чтобы это произошло (наименьшие полномочия!).
```
command="rsync --server -logDtpre.iLsfx --log-format=X --delete --delay-updates . /srv/fdroid-mirror.at.or.at/htdocs/fdroid/"
```
Единственная часть этой команды, которую можно настроить: конечный путь. Это может быть любой путь, но он должен указывать на каталог `/fdroid/` и иметь косую черту в конце. Если какой-либо из параметров *rsync* будет изменен, это нарушит настройку синхронизации.

В качестве дополнительной меры предосторожности должна быть учетная запись пользователя (например, `fdroid`), предназначенная для получения соединения *rsync/ssh*. Он должен иметь как можно меньше доступа. У него определенно не должно быть прав на запись в файл *authorized_keys*, так как это позволит злоумышленнику, получившему доступ на запись, добавить отдельную строку конфигурации ключа, которая обходит все перечисленные там ограничения. Это можно сделать, просто выполнив:
```
$ sudo chown root.root /home/fdroid/.ssh /home/fdroid/.ssh/authorized_keys
$ sudo chmod 0755 /home/fdroid/.ssh
$ sudo chmod 0644 /home/fdroid/.ssh/authorized_keys
```
