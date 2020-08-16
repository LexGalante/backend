from os import getenv

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from .logger import Logger
from resources.config import config


class DbContext():
    engine = None
    session: Session = None

    def factory_engine(self):
        self.engine = create_engine(config.CONNECTION_STRING, pool_pre_ping=True)

    def start(self):
        if self.session is None:
            self.factory_engine()
            self.session = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def finish(self):
        if self.session is not None:
            self.session.close()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()

    def try_commit(self):
        try:
            self.session.commit()
        except Exception as e:
            Logger.info(repr(e))
            self.session.rollback()
            raise e
        finally:
            self.session.close()
