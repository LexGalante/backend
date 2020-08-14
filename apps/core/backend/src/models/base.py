from sqlalchemy import Integer, Column


class Base():
    __table_args__ = {'schema': 'public'}

    id = Column(Integer, primary_key=True, index=True)

