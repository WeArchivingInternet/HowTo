# PyPI

## Установка [`bandersnatch`][bandersnatch]

[`bandersnatch`][bandersnatch] можно установить с помощью `pip`

```sh
pip install bandersnatch
```

## Настройка [`bandersnatch`][bandersnatch]

Сначала следует создать конфигурацию по умолчанию:

```sh
bandersnatch mirror
```

Эта команда создаст конфигурационный файл `/etc/bandersnatch.conf`. Путь к нему можно изменить с помощью опции `-c/--config`:

```sh
bandersnatch -c /path/to/config mirror
```

Можно отредактировать настройки - например, изменить директорию, в которой будут сохранены все необходимые данные.

## Скачивание данных

Нужно снова запустить команду из прошлого шага (если вы хотите использовать конфиг по другому пути, конечно, снова нужно использовать вышеуказанную опцию):

```sh
bandersnatch mirror
```

[bandersnatch]: https://github.com/pypa/bandersnatch