from typing import Annotated, Optional


from click import command
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, APIRouter, status, Depends
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_jwt_auth import AuthJWT

from app.db.users import db_actions
from app.db.users.models import User, Command, Tornament
from app.db.users.associative import UserCommandAssoc, Role
from app.db.base import get_db
from app.pydantic_models.users import UserModel, UserModelResponse, TokenModel, CommandModel, AddUserCommand


users_route = APIRouter(prefix="/users", tags=["Users"])


@users_route.post("/", status_code=status.HTTP_201_CREATED)
async def sign_up(user_model: UserModel, db: Annotated[AsyncSession, Depends(get_db)]):
    await db_actions.sign_up(**user_model.model_dump(), db=db)


@users_route.post("/token/", status_code=status.HTTP_202_ACCEPTED, response_model=TokenModel)
async def sign_in(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], Authorize: Annotated[AuthJWT, Depends()], db: Annotated[AsyncSession, Depends(get_db)]) -> str:
    user: Optional[User] = await db_actions.get_user(form_data.username, db)
    if not user or not user.verify_password(form_data.password):
        raise HTTPException(status_code=401,detail="Bad username or password")
    access_token = Authorize.create_access_token(subject=user.username)
    print(f'{access_token = }')
    return dict(access_token=access_token)


@users_route.get("/me/", status_code=status.HTTP_202_ACCEPTED, response_model=UserModelResponse)
async def get_user(username: Annotated[str, Depends(db_actions.decode_jwt)], db: Annotated[AsyncSession, Depends(get_db)]):
    return await db_actions.get_user(username=username, db=db)



@users_route.post("/commands/")
async def add_command(command_model: CommandModel, username: str = Depends(db_actions.decode_jwt), db: AsyncSession = Depends(get_db)):
    command = Command(**command_model.model_dump())
    user = await db.scalar(select(User).filter_by(username=username))
    command.users.append(user)
    db.add(command)
    user_command_assoc = await db.scalar(select(UserCommandAssoc).filter_by(user=user, command=command))
    user_command_assoc.role = Role.teamleader
    print(f"{user_command_assoc.role = }")
    await db.commit()


@users_route.patch("/commands/add-user-to-my-team/")
async def add_user_by_command(model: AddUserCommand, username: str = Depends(db_actions.decode_jwt), db: AsyncSession = Depends(get_db)):
    user_add = await db.scalar(select(User).filter_by(id=model.user_id))
    # user_command_assoc = await db.scalar(select(UserCommandAssoc).filter_by(user_id="fff1b45977b7454da0d2bdcebae74231", command_id=model.command_id))
    user_command_assoc = await db.scalar(select(UserCommandAssoc).filter(User.username=="string1", UserCommandAssoc.command_id==model.command_id))
    # print(f"{user_command_assoc.role = }")
    # user = await db.scalar(select(User).filter_by(username=username))
    # command = await db.scalar(select(Command).filter_by(id=model.command_id))
    print(f"{user_command_assoc = }")
    print(f"{user_command_assoc.role = }")
    print(f"{user_command_assoc.command.name = }")
    if not user_command_assoc or user_command_assoc.role != Role.teamleader:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not teamlead")

    user_command_assoc.command.users.append(user_add)
    await db.commit()

