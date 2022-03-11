# Local Docker Registry  

Инструкция на английском:  
https://docs.docker.com/registry/deploying/  

Ещё одна, но максимально кратко:  
https://docs.docker.com/registry/

Выжимка:  
Поднять сервер:  
```bash
docker run --rm -p 5000:5000 -v ПАПКА_ХОСТА:/var/lib/registry --name registry registry:2
```
**ПАПКА_ХОСТА** - место, где будут храниться image с хаба  

Загрузить image из хаба:  
```bash
docker pull ubuntu
```
Сделать тэг с указанием адреса локального регистри:
```bash
docker image tag ubuntu localhost:5000/myfirstimage
```
Запушить в локальный регистри:
```bash
docker push localhost:5000/myfirstimage
```

Для теста, что всё работает, можно поудалять локальные копии:
```bash
docker image remove ubuntu
docker image remove localhost:5000/myfirstimage
```
И вытянуть из регистри обратно:
```bash
docker pull localhost:5000/myfirstimage
```

###Внимание!
**Лучше запаковать регистри в архив, на тот случай, если потеряете image самого регистри из локального хранилища и не будет возможности его стянуть.**  

Пакуем:  
```bash
docker save registry:2 > registry2.tar
```
Распаковываем:
```bash
docker load --input registry2.tar
```
Аналогичный пожатый вариант:
```bash
docker save registry2 | gzip > registry2.tar.gz
docker load < registry2.tar.gz
```
Соответственно, нужно сохранить пакеты докера для вашей ОС  

Если уж принялись за бэкап регистри, то документацию тоже нужно бы склонить локально. Она есть на гитхабе(пока не пробовал запускать локально):  
https://github.com/docker/docker.github.io
