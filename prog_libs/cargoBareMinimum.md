# Настройка простого зеркала для crates.io

---

## Содержание:

* [Зеркалирование репозитория](#зеркалирование-репозитория)
* [Настройка индексов](#настройка-индексов)
* [Настройка файлового сервера](#настройка-файлового-сервера)

---

### Зеркалирование репозитория

Для начала нужно скачать скрипт [cargo_downloader.py](https://github.com/Kepler-Br/cargo_downloader).  
Как скачали, нужно перейти в директорию с скриптом и установить зависимости:
```bash
pip install -r requirements.txt
```
В репозитории есть инструкция по аргументам.  
Если не вдаваясь в подробности, то пойдёт следующая команда:  
```bash
python3 cargo_downloader.py Cargo.lock --output ./crates_io_mirror --err-log err.log
```
Если произойдёт какая ошибка при скачивании файлов, то о ней будет написано в файле `err.log`.  

---

### Настройка индексов

Далее необходимо форкнуть https://github.com/rust-lang/crates.io-index , скачать и поменять следующие параметры в файле `config.json`:

```json
{
  "dl": "http://localhost/api/v1/crates",
  "api": "http://localhost/"
}
```

Где `localhost` - адрес вашего файлового сервера, который мы поднимем позже.  
Пушим изменения в свой репозиторий и меняем содержимое файла `.cargo/.config.toml`:  
```toml
[source]

[source.mirror]
registry = "https://github.com/YOUR_NAME/crates.io-index.git"

[source.crates-io]
replace-with = "mirror"
```

Файл может быть как и в `~/.cargo/.config.toml`, так и в вашем проекте.  

---

### Настройка файлового сервера

***ВНИМАНИЕ!***  
***Выставлять порт файлового сервера из этой конфигурации в интернет без должного изучения документации nginx не рекомендуется!***  
***Открытые порты постоянно штурмуют всякого рода боты и есть вероятность того, что кто-то вломится на ваш сервер и поставит майнер или поломает сервер***

Создаём `docker-compose.yml`:
```yaml
version: "2.4"

services:
  nginx:
    image: nginx:1.21.6
    volumes:
      - "./data:/usr/share/nginx:ro"
      - "./conf:/etc/nginx/conf.d:ro"
    ports:
      - "8085:80"
```

Создаём файл `conf/nginx.conf`:
```
server {
 listen 80;
 server_name mirror.domain.com;
 root /usr/share/nginx/;

 location / {
   autoindex on;
 }
}
```

Кладём скаченные ранее пакеты из репозитория(папку `api`) в папку `data` рядом с сервером.  

```bash
docker-compose up
```

Пробуем билдить проект. Возможно, что нужно будет почистить `~/.cargo/registry`
