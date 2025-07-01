import enum
from enum import auto

from sqlalchemy import Table, Column, ForeignKey, Enum, Integer
from sqlalchemy.orm import mapped_column, relationship, Mapped

from app.db.base import Base


class Role(enum.Enum):
    teamleader = auto()
    member = auto()


class UserCommandAssoc(Base):
    __tablename__ = "user_command_assoc"

    user_id = Column(ForeignKey("users.id", ondelete="cascade"), primary_key=True)
    command_id = Column(ForeignKey("commands.id", ondelete="cascade"), primary_key=True)
    role = Column(Enum(Role), default=Role.member)
    user: Mapped["User"] = relationship(lazy="selectin")
    command: Mapped["Command"] = relationship(lazy="selectin")


class CommandTornamentAssoc(Base):
    __tablename__ = "command_tornament_assoc"

    command_id = Column(ForeignKey("commands.id", ondelete="cascade"), primary_key=True)
    tornament_id = Column(ForeignKey("tornaments.id", ondelete="cascade"), primary_key=True)
