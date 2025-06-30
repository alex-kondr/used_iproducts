import enum
from enum import auto

from sqlalchemy import Table, Column, ForeignKey, Enum, Integer
from sqlalchemy.orm import mapped_column

from app.db.base import Base


class Role(enum.Enum):
    teamleader = auto()
    member = auto()


class UserCommandAssoc(Base):
    __tablename__ = "user_command_assoc"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(ForeignKey("users.id"), primary_key=True)
    command_id = Column(ForeignKey("commands.id"), primary_key=True)
    role = Column(Enum(Role), default=Role.member)


# user_command_assoc = Table(
#     "user_command_assoc",
#     Base.metadata,
#     Column("user_id", ForeignKey("users.id"), primary_key=True),
#     Column("command_id", ForeignKey("commands.id"), primary_key=True),
#     Column("role", Enum(Role), default=Role.member)
# )

command_tornament_assoc = Table(
    "command_tornament_assoc",
    Base.metadata,
    Column("command_id", ForeignKey("commands.id"), primary_key=True),
    Column("tornament_id", ForeignKey("tornaments.id"), primary_key=True)
)
