from typing import Annotated, Optional
from fastapi import APIRouter, Cookie, Depends, HTTPException, status, Request, Form, Response
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from app.pydantic_models.users import UserForm


html_users_route = APIRouter(prefix="/web")
templates = Jinja2Templates(directory="app/templates/")


# @html_users_route.get("/")
# def func(response : Response):
#     response.set_cookie(key = "gfg_cookie_key", value = "gfg_cookie_value")
#     return {"message" : "Cookie is set on the browser"}

@html_users_route.get("/")
async def index(request: Request, gfg_cookie_key: Optional[str] = Cookie(None)):
    response = templates.TemplateResponse("index.html", context=dict(request=request))
    response.set_cookie(key="test", value="test--value")
    print(f"{request.cookies = }")
    print(f"{gfg_cookie_key = }")
    return response


@html_users_route.post("/")
async def sign_in(request: Request, response: Response, form: Annotated[UserForm, Form()]):
    print(f"Login: {form.username}\nPass: {form.password}")
    print(f"{request.cookies}")
    request.cookies["test2"] = "test_cook"
    response.set_cookie(key="test", value="test--")
    return templates.TemplateResponse("index.html", context=dict(request=request))


@html_users_route.get("/users/")
async def get_user(request: Request):
    return templates.TemplateResponse("users.html", context=dict(request=request))
