# Nimble пакеты

Задача: сдампать пакеты с [Nimble package directory](nimble.directory)

Дано:
- репозиторий https://github.com/nim-lang/packages со списком всех пакетов в формате json
- компилятор nim

Решение:

```sh
git clone https://github.com/nim-lang/packages
mkdir downloaded
touch load_all.nims
```
В файл `load_all.nims` вставляем код:

```nim
import json

const pkgs_source = slurp("./packages/packages.json")

let json_node = parseJson(pkgs_source)

assert json_node.kind == JArray

for pkg_node in json_node:
    assert pkg_node.kind == JObject
    try:
        let 
            name = pkg_node["name"].getStr
            get_url = pkg_node["url"].getStr
            get_method = pkg_node["method"].getStr

        if get_method != "git":
            continue
        
        echo name, get_url
        try:
            exec "git clone --recursive " & get_url & " ./downloaded/" & name
        except OSError:
            echo "OSError", name

    except KeyError:
        echo "KeyError", $pkg_node
        continue
```

Запускаем:
```sh
nim r load_all.nims
```

Всё, этого достаточно чтобы выгрузить большую часть пакетов с nimble.directory
