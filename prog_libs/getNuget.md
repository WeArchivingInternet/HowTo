# Nuget пакеты

Для шарпа самый популярный и большой пакетный менеджер это [Nuget](https://www.nuget.org/).

На github есть уже готовое решение для дампа nuget'а - взято с [этого репозитория](https://github.com/emgarten/NuGet.CatalogReader), проверил локально, все работает нормально.

Решение:
* Для начала качаем *dotnet cli*, по идее он есть в любом .NET SDK, рекомендую качать выше 5-ой версии (5-6, шарп работает еще быстрее).
* Выполняем две команды:

1. Качаем тулзу для мирроринга нугета: 
  * ```dotnet tool install -g nugetmirror```
2. Качаем все пакеты нугета в локальную папку (в данном случае это d:\tmp): 
  * ```NuGetMirror nupkgs https://api.nuget.org/v3/index.json -o d:\tmp```

Таким образом вы успешно выкачиваем вообще весь Nuget (297,064 уникальных пакетов на момент 07.03.2022).

Важный момент - насколько я понимаю, NugetMirror хранит tmp файлы для того чтобы знать какие пакеты уже скачались. По-этому опционально можно сделать запуск как Background Job раз в N часов, если конечно есть такое желание. 
