"""create table users

Revision ID: ed30e6582efd
Revises:
Create Date: 2020-08-20 19:58:45.287990

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ed30e6582efd'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("password", sa.String, nullable=False),
        sa.Column("active", sa.Boolean, nullable=False, default=True)
    )


def downgrade():
    op.drop_table("users")
