from typing import Generator

from resources.dbcontext import DbContext


def get_dbcontext() -> Generator:
    """
    Session DbContext
    """
    try:
        dbcontext: DbContext = DbContext()

        yield dbcontext
    finally:
        dbcontext.finish()



