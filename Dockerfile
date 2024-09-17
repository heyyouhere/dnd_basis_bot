# Используйте официальный образ Python как базовый
FROM python:3.11

# Установите рабочую директорию в контейнере
WORKDIR /usr/src/app

# Копируйте файлы зависимостей и установите зависимости
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Копируйте исходный код вашего приложения в контейнер
COPY . .

# Задайте команду для запуска вашего приложения
CMD [ "python", "./telegram_bot.py" ]
