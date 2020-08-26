from datetime import datetime

from sqlalchemy import (Boolean, Column, DateTime, ForeignKey, Integer,
                        MetaData, String, Table)

metadata = MetaData()

application_features = Table(
    "application_features",
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
