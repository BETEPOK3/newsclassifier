# TEAM-2 System

## Сборка/развертывание
```
docker-compose build
docker-compose up
```
## alembic
```
docker-compose exec web alembic revision --autogenerate -m "init"
docker-compose exec web alembic upgrade head  
```

Ссылка на модель векторизации для Word2Vec - https://drive.google.com/file/d/1AKB6tfWWlzHEBgrwojkkvHot6Jdfy00T/view?usp=sharing
