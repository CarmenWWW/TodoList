# models.py

from sqlalchemy.schema import Column
from sqlalchemy.types import String, Integer, Enum
from database import Base
import enum


class TodoInfo(Base):
    __tablename__ = "todo"

    id = Column(Integer, primary_key=True, index=True)
    item = Column(String)

