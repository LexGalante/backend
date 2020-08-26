from sqlalchemy import Boolean, Column, Integer, MetaData, String, Table

metadata = MetaData()

users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("email", String(250), unique=True, index=True, nullable=False),
    Column("password", String, nullable=False),
    Column("active", Boolean, nullable=False, default=True)
)
