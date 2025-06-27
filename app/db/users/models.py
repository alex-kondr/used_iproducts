from uuid import uuid4
from datetime import datetime, timezone, timedelta

import fastapi_jwt_auth
from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from passlib.context import CryptContext
import jwt 
from fastapi_jwt_auth import AuthJWT

from app.config import settings
from app.db.base import Base


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(Base):
    __tablename__ = "users"
    
    id: Mapped[str] = mapped_column(String(100), primary_key=True)
    username: Mapped[str] = mapped_column(String(30), unique=True, index=True)
    password_: Mapped[str] = mapped_column(String(100))
    active: Mapped[Boolean] = mapped_column(Boolean(), default=True)
    
    def __init__(self, **kwargs):
        self.id = uuid4().hex
        super().__init__(**kwargs)
        
    
    @property
    def password(self):
        return self.password_
    
    
    @password.setter
    def password(self, pwd):
       self.password_ = pwd_context.hash(pwd)
        
    
    def verify_password(self, pwd) -> bool:
        return pwd_context.verify(pwd, self.password_)
    
    
    # def create_token(self):
    #     access_token = Authorize.create_access_token(subject=user.username)
    #     return dict(access_token=access_token)
        
    
