from typing import List

from models.environment import Environment
from resources.dbcontext import DbContext
from .repository import Repository


class EnvironmentRepository(Repository):
    def __init__(self, dbcontext: DbContext):
        super().__init__(dbcontext)

    def get_all(self) -> List[Environment]:
        return self._db.session.query(Environment).all()
