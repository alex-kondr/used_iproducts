import asyncio

from fastapi import FastAPI, HTTPException, status, Depends, Request
from fastapi.responses import JSONResponse
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.gzip import GZipMiddleware
import uvicorn
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from fastapi.staticfiles import StaticFiles

from app.routes.users import users_route
from app.html_routes.users import html_users_route
from app.websocket.users import websocket_route
from app.db.base import create_db
from app.config import settings



app = FastAPI()
# app.add_middleware(HTTPSRedirectMiddleware)
# app.add_middleware(TrustedHostMiddleware, allowed_hosts=["127.0.0.1"])
# app.add_middleware(GZipMiddleware)
app.include_router(users_route)
app.include_router(html_users_route)
app.include_router(websocket_route)
app.mount("/static", StaticFiles(directory="app/static/"), name="static")


@AuthJWT.load_config
def get_config():
    return settings


# print(AuthJWT._access_token_expires)


@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )


if __name__ == "__main__":
#     # asyncio.run(create_db())
    uvicorn.run("main:app", reload=True)