# Телеграм-бот на Python ❤️
Ниже представлена инструкция по запуску бота.

1. cp .env.template .env
2. docker-compose build --no-cache
3. docker-compose up
4. docker-compose exec db psql -U postgres -c "CREATE DATABASE gino;"
5. docker-compose stop && docker-compose up --build