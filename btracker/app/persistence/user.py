from sqlalchemy import (
    Column, Integer, BigInteger, String, Date,
    UniqueConstraint, update,
    or_,
    distinct
)
from sqlalchemy.dialects.postgresql import (
    UUID, insert
)

from app.db import Base, Session


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
