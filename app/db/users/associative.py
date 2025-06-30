from sqlalchemy import Table, Column, ForeignKey

from app.db.base import Base


user_command_assoc = Table(
    "user_command_assoc",
    Base.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("command_id", ForeignKey("commands.id"), primary_key=True)
)

command_tornament_assoc = Table(
    "command_tornament_assoc",
    Base.metadata,
    Column("command_id", ForeignKey("commands.id"), primary_key=True),
    Column("tornament_id", ForeignKey("tornaments.id"), primary_key=True)
)
