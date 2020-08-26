from datetime import datetime

from sqlalchemy import (Boolean, Column, DateTime, ForeignKey, Integer,
                        MetaData, String, Table)

metadata = MetaData()

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
