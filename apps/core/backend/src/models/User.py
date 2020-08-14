from sqlalchemy import Boolean, Column, String

from .base import Base


class User(Base):
    __tablename__ = "users"

    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    active = Column(Boolean, nullable=False, default=True)
