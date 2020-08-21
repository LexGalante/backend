from sqlalchemy import Column, String, Boolean

from .base import Base


class Environment(Base):
    name = Column(String(3), nullable=False)
    description = Column(String(250), nullable=False)
    active = Column(Boolean, nullable=False, default=True)
