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


#--------------------------------------------------------------------------------------------------------------------
AUTH_SERVICE = "http://localhost:8001"#------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------


@app.api_route("/api/auth/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"])
async def proxy_auth(request: Request, path: str):
    url = f"{AUTH_SERVICE}/api/auth/{path}"
    return await proxy_request(request, url)

@app.api_route("/api/users/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"])
async def proxy_users(request: Request, path: str):
    url = f"{AUTH_SERVICE}/api/users/{path}"
    return await proxy_request(request, url)

@app.api_route("/api/users", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"])
async def proxy_users_root(request: Request):
    url = f"{AUTH_SERVICE}/api/users"
    return await proxy_request(request, url)


#--------------------------------------------------------------------------------------------------------------------
PRODUCT_SERVICE = "http://localhost:8002"#---------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------


@app.api_route("/api/products/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"])
async def proxy_products(request: Request, path: str):
    url = f"{PRODUCT_SERVICE}/api/products/{path}"
    return await proxy_request(request, url)

@app.api_route("/api/products", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"])
async def proxy_products_root(request: Request):
    url = f"{PRODUCT_SERVICE}/api/products"
    return await proxy_request(request, url)
async def proxy_request(request: Request, url: str):
    body = await request.body()
    headers = dict(request.headers)
    headers.pop("host", None)

    async with httpx.AsyncClient() as client:
        response = await client.request(
            method=request.method,
            url=url,
            headers=headers,
            content=body,
            params=request.query_params,
        )
    return __import__("starlette").responses.Response(
        content=response.content,
        status_code=response.status_code,
        headers=dict(response.headers),
    )

@app.get("/")
def home():
    return {"message": "API Gateway работает!"}