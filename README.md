# Guide

1) В консоли github устанавливаем репозиторий и называем его "origin":
git remote add origin https://github.com/devFF/projects
2) Закачиваем проект с локального хранилища в репозиторий:
git push -u origin master
2.1) Если нужно переписать ветку репозитория, тогда вместо ключа -u, нужно выбрать -f или --force. Делать только в карйнем случае
3) Загружаем проект с репозитория на локальное хранилище: git clone https://github.com/devFF/projects
4) git status
5) git add .
6) git commit "some text"
7) git push -u origin master
