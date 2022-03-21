# Архивирование различных хостингов репозиториев Git

## GitHub

Можно воспользоваться скриптом [starred.py](https://git.sr.ht/~handlerug/starred.py).
[Его копия есть в этом репозитории.](./starred.py)
Скрипт умеет скачивать списки репозиториев и звёздочки пользователей.
Для работы нужен Python >= 3.4 и, очевидно, Git.

Пример работы:

```sh
# Выгрузить список репозиториев пользователя octocat в файл repos.json:
./starred.py user octocat repos.json
# Выгрузить список репозиториев организации github в файл repos.json:
./starred.py org github repos.json
# Выгрузить звёздочки пользователя octocat в файл stars.json:
./starred.py stars octocat stars.json
```

После выгрузки соответствующий JSON-файлик можно передать на архивацию:

```sh
mkdir repos && cd repos
# Скачать репозитории из файла repos.json:
../starred.py clone ../repos.json
```

Авторизация будет игнорирована, и такие репозитории будут пропущены. TODO: добавить поддержку авторизации
