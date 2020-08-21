"""create table application_environments

Revision ID: 65612885ab31
Revises: 1f94bf3b665e
Create Date: 2020-08-20 23:20:14.817308

"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime


# revision identifiers, used by Alembic.
revision = '65612885ab31'
down_revision = '1f94bf3b665e'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "application_environments",
        sa.Column("id", sa.Integer, primary_key=True, index=True),
        sa.Column("application_id", sa.Integer, sa.ForeignKey("applications.id")),
        sa.Column("environment_id", sa.Integer, sa.ForeignKey("environments.id")),
        sa.Column("name", sa.String(250), index=True, nullable=False),
        sa.Column("enable", sa.Boolean, nullable=False, default=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, default=datetime.now()),
        sa.Column("created_by", sa.Integer, sa.ForeignKey("users.id")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, default=datetime.now()),
        sa.Column("updated_by", sa.Integer, sa.ForeignKey("users.id"))
    )


def downgrade():
    op.drop_table("application_environments")
