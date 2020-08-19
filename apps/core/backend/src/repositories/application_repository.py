from typing import List

from models.application import Application, ApplicationUser
from models.user import User
from resources.dbcontext import DbContext

from .repository import Repository


class ApplicationRepository(Repository):
    def __init__(self, dbcontext: DbContext):
        super().__init__(dbcontext)

    def get_all_by_user(self, user: User) -> List[Application]:
        return self._db.session.query(
            Application,
            ApplicationUser
        ).filter(ApplicationUser.user_id == user.id).all()

    def get_by_name(self, name: str, user: User) -> Application | None:
        return self._db.session.query(
            Application,
            ApplicationUser
        ).filter(Application.name == name).filter(ApplicationUser.user_id == user.id).first()

    def create(self, application: Application):
        self._db.session.add(application)

    def name_exists(self, name: str) -> bool:
        return self._db.session.query(Application).filter(Application.name == name).count() > 0

