from sqlalchemy import Column, ForeignKey, Integer, MetaData, Table

metadata = MetaData()

application_users = Table(
    "application_users",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("application_id", Integer, ForeignKey("applications.id")),
    Column("user_id", Integer, ForeignKey("users.id"))
)
