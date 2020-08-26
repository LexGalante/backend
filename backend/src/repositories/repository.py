from resources.dbcontext import DbContext


class Repository():
    def __init__(self, db: DbContext):
        self._db: DbContext = db
        self._db.start()

    def close(self):
        self._db.finish()
