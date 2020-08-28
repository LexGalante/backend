from datetime import datetime
from databases import Database
from sqlalchemy import (Boolean, Column, DateTime, ForeignKey, Integer,
                        MetaData, String, Table)

from .config import CONNECTION_STRING, MAX_CONNECTIONS, MIN_CONNECTIONS

database: Database = Database(CONNECTION_STRING, min_size=int(MIN_CONNECTIONS), max_size=int(MAX_CONNECTIONS))
metadata = MetaData()


async def database_connect():
    await database.connect()


async def database_disconnect():
    await database.disconnect()


users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("email", String(250), unique=True, index=True, nullable=False),
    Column("password", String, nullable=False),
    Column("active", Boolean, nullable=False, default=True)
)

environments = Table(
    "environments",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("name", String, unique=True, index=True, nullable=False),
    Column("description", String, nullable=False),
    Column("active", Boolean, nullable=False, default=True)
)

applications = Table(
    "applications",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("name", String(30), nullable=False, unique=True, index=True),
    Column("real_name", String(250), nullable=False),
    Column("model", Integer, nullable=False, default=1),
    Column("description", String(250), nullable=False),
    Column("details", String(5000), nullable=True),
    Column("active", Boolean, nullable=False, default=True),
    Column("created_at", DateTime(timezone=True),
           nullable=False, default=datetime.now()),
    Column("created_by", Integer, ForeignKey("users.id")),
    Column("updated_at", DateTime(timezone=True),
           nullable=False, default=datetime.now()),
    Column("updated_by", Integer, ForeignKey("users.id"))
)

application_users = Table(
    "application_users",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("application_id", Integer, ForeignKey("applications.id")),
    Column("user_id", Integer, ForeignKey("users.id"))
)

application_features = Table(
    "application_features",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("application_id", Integer, ForeignKey("applications.id")),
    Column("environment_id", Integer, ForeignKey("environments.id")),
    Column("name", String(250), nullable=False),
    Column("enable", Boolean, nullable=False, default=False),
    Column("created_at", DateTime(timezone=True), nullable=False, default=datetime.now()),
    Column("created_by", Integer, ForeignKey("users.id")),
    Column("updated_at", DateTime(timezone=True), nullable=False, default=datetime.now()),
    Column("updated_by", Integer, ForeignKey("users.id"))
)
