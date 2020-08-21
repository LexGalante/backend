"""create table application_features

Revision ID: c45ac8c5d012
Revises: c99749a55f39
Create Date: 2020-08-21 12:28:47.966476

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.orm import Session
from datetime import datetime


# revision identifiers, used by Alembic.
revision = 'c45ac8c5d012'
down_revision = 'c99749a55f39'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "application_features",
        sa.Column("id", sa.Integer, primary_key=True, index=True),
        sa.Column("application_id", sa.Integer, sa.ForeignKey("applications.id")),
        sa.Column("environment_id", sa.Integer, sa.ForeignKey("environments.id")),
        sa.Column("name", sa.String(250), nullable=False),
        sa.Column("enable", sa.Boolean, nullable=False, default=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, default=datetime.now()),
        sa.Column("created_by", sa.Integer, sa.ForeignKey("users.id")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, default=datetime.now()),
        sa.Column("updated_by", sa.Integer, sa.ForeignKey("users.id"))
    )

    op.create_unique_constraint(
        "application_features_un",
        "application_features",
        ["application_id", "environment_id", "name"],
        schema="public"
    )

    bind = op.get_bind()
    session = Session(bind=bind)
    session.execute(
        "INSERT INTO application_features (application_id, environment_id, name, enable, created_at, created_by, updated_at, updated_by) VALUES (:application_id, :environment_id, :name, :enable, :created_at, :created_by, :updated_at, :updated_by)",
        {
            "application_id": 1,
            "environment_id": 1,
            "name": "notification",
            "enable": True,
            "created_at": datetime.now(),
            "created_by": 1,
            "updated_at": datetime.now(),
            "updated_by": 2
        }
    )


def downgrade():
    op.drop_table("application_features")
