# API Gateway — единая точка входа

## Описание
API Gateway принимает все запросы от фронтенда и проксирует их в соответствующие микросервисы. Обеспечивает единый URL для клиента и централизованный CORS.

## Пакеты
- Python 
- FastAPI 
- HTTPX 

### Локально/Запуск
pip install -r requirements.txt
uvicorn app:app --reload --port 8000

### Docker/Запуск
docker build -t api-gateway .
docker run -d -p 8000:8000 --name gateway-container api-gateway

### Docker Compose (все сервисы)/Запуск
docker-compose up -d --build

## Маршрутизация

| Путь | Сервис | Порт |
|------|--------|------|
| /api/auth/* | Auth Service | 8001 |
| /api/users/* | Auth Service | 8001 |
| /api/products/* | Product Service | 8002 |
| /api/cart/* | Cart-Favorite Service | 8003 |
| /api/favorites/* | Cart-Favorite Service | 8003 |
| /api/orders/* | Order Service | 8004 |

## URL
http://localhost:8000/docs