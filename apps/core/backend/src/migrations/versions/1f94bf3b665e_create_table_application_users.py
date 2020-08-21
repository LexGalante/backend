"""create table application_users

Revision ID: 1f94bf3b665e
Revises: 91663f1db7c5
Create Date: 2020-08-20 23:17:22.422958

"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime


# revision identifiers, used by Alembic.
revision = '1f94bf3b665e'
down_revision = '91663f1db7c5'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "application_users",
        sa.Column("id", sa.Integer, primary_key=True, index=True),
        sa.Column("application_id", sa.Integer, sa.ForeignKey("applications.id"), primary_key=True),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id"), nullable=False, primary_key=True)
    )


def downgrade():
    op.drop_table("application_users")
