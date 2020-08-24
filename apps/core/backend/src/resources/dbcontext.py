import logging

from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session, sessionmaker

from resources.config import CONNECTION_STRING, CONNECTION_STRING_TEST


class DbContext():
    engine = None
    session: Session = None
    in_testing: bool = False
    logger = logging.getLogger(__name__)

    def __init__(self, in_testing: bool = False):
        self.in_testing = in_testing

    def factory_engine(self):
        if self.in_testing:
            self.engine = create_engine(CONNECTION_STRING_TEST, pool_pre_ping=True)
        else:
            self.engine = create_engine(CONNECTION_STRING, pool_pre_ping=True)

    def start(self):
        if self.session is None:
            self.factory_engine()
            session_local = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
            self.session = session_local()

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
            self.logger.info(repr(e))
            self.session.rollback()
            raise e
        finally:
            self.session.close()

    def execute(self, sql: str, parameters: dict):
        result = self.session.execute(sql, parameters)

        return result
