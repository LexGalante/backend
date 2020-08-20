import logging

from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session, sessionmaker

from resources.config import CONNECTION_STRING


class DbContext():
    engine = None
    session: Session = None
    logger = logging.getLogger(__name__)

    def factory_engine(self):
        self.engine = create_engine(CONNECTION_STRING, pool_pre_ping=True)

    def start(self):
        if self.session is None:
            self.factory_engine()
            SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
            self.session = SessionLocal()

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

    @staticmethod
    def raw(sql: str):
        sql = text(sql)
        engine = create_engine(CONNECTION_STRING, pool_pre_ping=True)
        result = engine.execute(sql)

        return result
