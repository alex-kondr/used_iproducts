from typing import Annotated, Optional

import jwt
from jwt.exceptions import InvalidTokenError
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_jwt_auth import AuthJWT
import jwt

from app.db.users.models import User, Command, Tornament, Result
# from app.db.base import get_db
from app.config import settings


def get_username(token):
    # try:
    payload = jwt.decode(token, settings.authjwt_secret_key, algorithms=[settings.algorithm])
    print(payload)
    return payload.get("sub")
    # except:
    #     HTTPException(status_code=status.HTTP_403_FORBIDDEN)


def decode_jwt(Authorize: Annotated[AuthJWT, Depends()], token: Annotated[str, Depends(OAuth2PasswordBearer(tokenUrl="/users/token/"))]):
    Authorize.jwt_required()
    return Authorize.get_jwt_subject()
    
    
async def get_user(username: str, db: AsyncSession) -> Optional[User]:
    query = select(User).filter_by(username=username)
    result = await db.execute(query)
    return result.scalar_one_or_none()
    

async def sign_up(username:str, password:str, db: AsyncSession):
    user = await get_user(username=username, db=db)
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Такий користувач вже існує.")
    
    user = User(username=username, password=password)
    db.add(user)
    await db.commit()
    

# async def sign_in(username: str, password: str, db: AsyncSession) -> str:
#     user = await get_user(username=username, db=db)
#     if not user or not user.verify_password(password):
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Логін або пароль не правильний.")
#     return user.create_token()