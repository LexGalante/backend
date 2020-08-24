from resources.dbcontext import DbContext


def execute_clean_data(sql: str, parameters: dict):
    dbcontext: DbContext = DbContext(in_testing=True)
    try:
        dbcontext.start()
        dbcontext.execute(sql, parameters)
        dbcontext.commit()
    finally:
        dbcontext.finish()
