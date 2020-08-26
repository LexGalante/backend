"""create table applications

Revision ID: 6cbae6678e5c
Revises: b15b0aa87418
Create Date: 2020-08-21 12:12:17.286672

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.orm import Session
from datetime import datetime


# revision identifiers, used by Alembic.
revision = '6cbae6678e5c'
down_revision = 'b15b0aa87418'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "applications",
        sa.Column("id", sa.Integer, primary_key=True, index=True),
        sa.Column("name", sa.String(30), nullable=False, unique=True, index=True),
        sa.Column("real_name", sa.String(250), nullable=False),
        sa.Column("model", sa.Integer, nullable=False, default=1),
        sa.Column("description", sa.String(250), nullable=False),
        sa.Column("details", sa.String(5000), nullable=True),
        sa.Column("active", sa.Boolean, nullable=False, default=True),
        sa.Column("created_at", sa.DateTime(timezone=True),
                  nullable=False, default=datetime.now()),
        sa.Column("created_by", sa.Integer, sa.ForeignKey("users.id")),
        sa.Column("updated_at", sa.DateTime(timezone=True),
                  nullable=False, default=datetime.now()),
        sa.Column("updated_by", sa.Integer, sa.ForeignKey("users.id"))
    )

    bind = op.get_bind()
    session = Session(bind=bind)
    session.execute(
        """
        INSERT INTO applications
            (name, real_name, model, description, details, active, created_at, created_by, updated_at, updated_by)
        VALUES
            (:name, :real_name, :model, :description, :details, :active, :created_at, :created_by, :updated_at, :updated_by)
        """, {
            "name": "netflix",
            "real_name": "Netflix",
            "model": 1,
            "description": "Streaming movies, series, animes etc...",
            "details": "https://netflix.com.br",
            "active": True,
            "created_at": datetime.now(),
            "created_by": 1,
            "updated_at": datetime.now(),
            "updated_by": 1
        }
    )
    session.execute(
        """
        INSERT INTO applications
            (name, real_name, model, description, details, active, created_at, created_by, updated_at, updated_by)
        VALUES
            (:name, :real_name, :model, :description, :details, :active, :created_at, :created_by, :updated_at, :updated_by)
        """, {
            "name": "whats_app",
            "real_name": "Whats App",
            "model": 2,
            "description": "Sendind and receive instant messages, videos, gifs and docs",
            "details": "https://whatsapp.com.br",
            "active": True,
            "created_at": datetime.now(),
            "created_by": 2,
            "updated_at": datetime.now(),
            "updated_by": 2
        }
    )
    session.execute(
        """
        INSERT INTO applications
            (name, real_name, model, description, details, active, created_at, created_by, updated_at, updated_by)
        VALUES
            (:name, :real_name, :model, :description, :details, :active, :created_at, :created_by, :updated_at, :updated_by)
        """, {
            "name": "microsoft_office",
            "real_name": "Microsoft Office",
            "model": 2,
            "description": "Docs, sheets, presents, email etc...",
            "details": "https://msoffice365.com.br",
            "active": True,
            "created_at": datetime.now(),
            "created_by": 3,
            "updated_at": datetime.now(),
            "updated_by": 3
        }
    )


def downgrade():
    op.drop_table("applications")
