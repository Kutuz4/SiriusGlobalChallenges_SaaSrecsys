
# Используйте официальный образ Python
FROM python:3.8

# Установить рабочую директорию в контейнере
WORKDIR /usr/src/app

# Установить зависимости
# Копировать requirements.txt и установить зависимости с помощью pip
COPY . .
RUN pip install --no-cache-dir -r ./requirements.txt
# Копировать остальные исходные файлы в рабочую директорию контейнера
EXPOSE 5000
# Указать Docker запустить эту команду при запуске контейнера
CMD [ "python", "./collaborative_baseline_new.py"]

