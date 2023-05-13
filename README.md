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