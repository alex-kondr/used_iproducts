from typing import Annotated, Optional
from datetime import timedelta

from pydantic import BaseModel, Field
from fastapi import Form


class UserModel(BaseModel):
    username: str
    password: str
    

class UserModelResponse(BaseModel):
    id: str
    username: str
    active: bool
    
    
class TokenModel(BaseModel):
    access_token: str
    token_type: str = "Bearer"


class UserForm(BaseModel):
    username: str = Field(...)
    password: str = Field(...)


class CommandModel(BaseModel):
    name: str
    private: bool


class AddUserCommand(BaseModel):
    user_id: str
    command_id: str
