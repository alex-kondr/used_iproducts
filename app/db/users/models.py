from uuid import uuid4
from datetime import datetime, timezone, timedelta
from typing import List

import fastapi_jwt_auth
from sqlalchemy import ForeignKey, String, Boolean, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship
from passlib.context import CryptContext
import jwt 
from fastapi_jwt_auth import AuthJWT

from app.config import settings
from app.db.base import Base
from app.db.users.associative import UserCommandAssoc, command_tornament_assoc


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


class Command(Base):
    __tablename__ = "commands"

    id: Mapped[str] = mapped_column(String(100), primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)
    users: Mapped[List[User]] = relationship(secondary=UserCommandAssoc.__tablename__, back_populates="commands")
    # data_assoc_id: Mapped[int] = relationship(ForeignKey(UserCommandAssoc.id))
    data_assoc: Mapped[UserCommandAssoc] = relationship()

    def __init__(self, **kwargs):
        self.id = uuid4().hex
        super().__init__(**kwargs)


class Tornament(Base):
    __tablename__ = "tornaments"

    id: Mapped[str] = mapped_column(String(100), primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)
    commands: Mapped[List[Command]] = relationship(secondary=command_tornament_assoc)

    def __init__(self, **kwargs):
        self.id = uuid4().hex
        super().__init__(**kwargs)


class Result(Base):
    __tablename__ = "results"

    id: Mapped[str] = mapped_column(String(100), primary_key=True)
    rating: Mapped[float] = mapped_column()
    tornament_id: Mapped[str] = mapped_column(String(100), ForeignKey(Tornament.id))
    command_id: Mapped[str] = mapped_column(String(100), ForeignKey(Command.id))
    tornament: Mapped[Tornament] = relationship()
    command: Mapped[Command] = relationship()

    def __init__(self, **kwargs):
        self.id = uuid4().hex
        super().__init__(**kwargs)
