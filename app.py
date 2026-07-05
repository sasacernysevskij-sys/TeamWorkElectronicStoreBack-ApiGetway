from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import httpx

app = FastAPI(title="API Gateway", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Сервисы
AUTH_SERVICE = "http://auth:8001"
PRODUCT_SERVICE = "http://product:8002"
CART_FAVORITE_SERVICE = "http://cart:8003"
ORDER_SERVICE = "http://order:8004"


# ==================== AUTH ====================
@app.api_route("/api/auth/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"])
async def proxy_auth(request: Request, path: str):
    url = f"{AUTH_SERVICE}/api/auth/{path}"
    return await proxy_request(request, url)

@app.api_route("/api/auth", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"])
async def proxy_auth_root(request: Request):
    url = f"{AUTH_SERVICE}/api/auth"
    return await proxy_request(request, url)

@app.api_route("/api/users/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"])
async def proxy_users(request: Request, path: str):
    url = f"{AUTH_SERVICE}/api/users/{path}"
    return await proxy_request(request, url)

@app.api_route("/api/users", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"])
async def proxy_users_root(request: Request):
    url = f"{AUTH_SERVICE}/api/users"
    return await proxy_request(request, url)


# ==================== PRODUCTS ====================
@app.api_route("/api/products/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"])
async def proxy_products(request: Request, path: str):
    url = f"{PRODUCT_SERVICE}/api/products/{path}"
    return await proxy_request(request, url)

@app.api_route("/api/products", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"])
async def proxy_products_root(request: Request):
    url = f"{PRODUCT_SERVICE}/api/products"
    return await proxy_request(request, url)


# ==================== CART ====================
@app.api_route("/api/cart/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"])
async def proxy_cart(request: Request, path: str):
    url = f"{CART_FAVORITE_SERVICE}/api/cart/{path}"
    return await proxy_request(request, url)

@app.api_route("/api/cart", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"])
async def proxy_cart_root(request: Request):
    url = f"{CART_FAVORITE_SERVICE}/api/cart"
    return await proxy_request(request, url)


# ==================== FAVORITES ====================
@app.api_route("/api/favorites/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"])
async def proxy_favorites(request: Request, path: str):
    url = f"{CART_FAVORITE_SERVICE}/api/favorites/{path}"
    return await proxy_request(request, url)

@app.api_route("/api/favorites", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"])
async def proxy_favorites_root(request: Request):
    url = f"{CART_FAVORITE_SERVICE}/api/favorites"
    return await proxy_request(request, url)


# ==================== ORDERS ====================
@app.api_route("/api/orders/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"])
async def proxy_orders(request: Request, path: str):
    url = f"{ORDER_SERVICE}/api/orders/{path}"
    return await proxy_request(request, url)

@app.api_route("/api/orders", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"])
async def proxy_orders_root(request: Request):
    url = f"{ORDER_SERVICE}/api/orders"
    return await proxy_request(request, url)


# ==================== PROXY ====================
async def proxy_request(request: Request, url: str):
    body = await request.body()
    headers = dict(request.headers)
    headers.pop("host", None)
    
    # Логирование
    print(f"ПРОКСИ: {request.method} {url}")
    print(f"Заголовки: {headers}")

    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.request(
            method=request.method,
            url=url,
            headers=headers,
            content=body,
            params=request.query_params,
        )
    
    print(f"ОТВЕТ: {response.status_code}")
    
    return __import__("starlette").responses.Response(
        content=response.content,
        status_code=response.status_code,
        headers=dict(response.headers),
    )
@app.get("/")
def home():
    return {"message": "API Gateway работает!"}