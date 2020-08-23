import logging

from alchemy_mock.mocking import UnifiedAlchemyMagicMock


class FakeDbContext:
    session: UnifiedAlchemyMagicMock = None
    logger = logging.getLogger(__name__)

    def start(self):
        if self.session is None:
            self.session = UnifiedAlchemyMagicMock()

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
