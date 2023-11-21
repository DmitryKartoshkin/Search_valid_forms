# Web-приложение для определения заполненных форм.

## Задание
### https://docs.google.com/document/d/1fMFwPBs53xzcrltEFOpEG4GWTaQ-5jvVLrNT6_hmC7I/edit

## 1. Зависимости
Для проекта потребуется:
- Python 3.11
- Docker Desktop
- Git

## 2. Запуск приложения
Запуск и сборка приложения и базы данных происходит с помощью команды через docker-compose:
```shell
docker-compose -f docker-compose.yml up --build 
```

## 3. запуск тестов
Запуск тестов происходит через терминале git bash командой:
```shell
./run_tests.sh
```
После запуска скрипта происходит сборка контейнеров с БД и приложением, прогон тестов, и удаление контейнеров 
