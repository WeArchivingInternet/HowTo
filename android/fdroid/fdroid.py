#!/usr/bin/python3
#С помощью wget скачивает файлы основываясь на index.xml файле репозитория.
#linux-only, потому что Windows не может найти wget (хотя он есть)
#index.xml скачивается дважды, т.к. лень делать путь к уже скачанному
#3.7

import sys, os
import xml.etree.ElementTree as ET

repoMetaInfoFiles = ["index.html","index.xml","index.jar","categories.txt","index-v1.jar","index-v1.json","index.png","index.css", "status/running.json", "status/update.json"]
iconsDirs = ["icons-120/", "icons-160/", "icons-240/","icons-320/","icons-480/", "icons-640/", "icons/"]

if (len(sys.argv)<2 or sys.argv[1][-1]!='/'):
    print('''usage: f-droid.py <url>
URL must end with '/'
Options:
    -ni - Don't download images
    -ns - Don't download sources
    -na - Don't download apks
    -nm - Don't download repository metainfo files
    -wq - Quiet wget''')
    exit(2)

url = sys.argv[1]

def downloadFile(fileUrl):
    #Параметр -x форсирует создание директорий
    #Параметр -N - скачивание файла только если его нет или если он обновился на сервере.
    if("-wq" in sys.argv):
        os.system("wget -xNq " + fileUrl)
    else:
        os.system("wget -xN " + fileUrl)

def getIndexXmlTree():
    print("Parsing repo index.xml")
    tree = ET.parse('index.xml')
    root = tree.getroot()
    return root

def downloadMetaInfoFiles():
    for i in range(len(repoMetaInfoFiles)):
        downloadFile(url+repoMetaInfoFiles[i])

def downloadApks(root):
    apps = root.findall('./application')
    print("Apps in repo: " + str(len(apps)))
    apks = []
    for app in apps:
        for pack in app.iter('package'):
            apks.append(pack.find("apkname").text)

    for apk in apks:
        downloadFile(url+apk)

def downloadSources(root):
    apps = root.findall('./application')
    print("Apps in repo: " + str(len(apps)))
    srcs = []

    for app in apps:
        for pack in app.iter('package'):
            srcElem = pack.find("srcname")
            #Не факт что в репозитории будет исходный код приложения.
            if (type(srcElem) == type(None)):
                continue
            else:
                srcs.append(srcElem.text)

    for srcfile in srcs:
        downloadFile(url+srcfile)

def downloadImages(root):
    apps = root.findall('./application')
    print("Apps in repo: " + str(len(apps)))
    imgs = []

    for app in apps:
        iconElem = app.find("icon")
        #Не во всех приложениях есть иконка
        if(type(iconElem) == type(None)):
            continue
        else:
            imgs.append(iconElem.text)

    for img in imgs:
        for iconsDir in iconsDirs:
            downloadFile(url+iconsDir+img)
        

print("Downloading repo index.xml")
if("-wq" in sys.argv):
    os.system("wget -Nq " + url + "index.xml")
else:
    os.system("wget -N " + url + "index.xml")

index = getIndexXmlTree()

if("-nm" not in sys.argv):
    downloadMetaInfoFiles()
    print("MetaInfo files downloaded")
if("-ni" not in sys.argv):
    downloadImages(index)
    print("Images downloaded")
if("-na" not in sys.argv):
    downloadApks(index)
    print("APKs downloaded")
if("-ns" not in sys.argv):
    downloadSources(index)
    print("Src downloaded")

os.remove('index.xml')
