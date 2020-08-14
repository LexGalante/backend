from os import getenv

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from .logger import Logger


class DbContext():
    connection_string: str = getenv("CONNECTION_STRING")
    engine = None
    session: Session = None

    def factory_engine(self):
        self.engine = create_engine(self.connection_string, pool_pre_ping=True)

    def start(self):
        if self.session is not None:
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
