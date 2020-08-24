from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy import Column, Integer


@as_declarative()
class Base:
    __table_args__ = {'schema': 'public'}

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
