from sqlalchemy import Boolean, Column, Integer, String, Table, MetaData

metadata = MetaData()

environments = Table(
    "environments",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("name", String, unique=True, index=True, nullable=False),
    Column("description", String, nullable=False),
    Column("active", Boolean, nullable=False, default=True)
)
