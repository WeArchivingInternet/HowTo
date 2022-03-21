# Как архивировать
* CentOS
  - [Вариант с reposync + nginx](https://hamsterden.ru/local-repository-for-yum/)

* Termux
  - rsync
    ```sh
    RSYNC_PASSWORD=termuxmirror rsync -avz  --delete --progress rsync@grimler.se::termux YOUR_PATH
    ```
* yandex mirror
  - rsync
    ```sh
    rsync -avz  --delete --progress rsync://mirror.yandex.ru/YOUR_OS/ YOUR_PATH
    ```

# Список зеркал репозиториев на территории РФ
* https://mirror.yandex.ru/ - есть практически всё: от арчлинукса до слаки.
* https://mirror.truenetwork.ru/
* https://mirror.surf/
* http://mirrors.powernet.com.ru/
