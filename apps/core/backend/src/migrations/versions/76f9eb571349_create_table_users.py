"""create table users

Revision ID: 76f9eb571349
Revises:
Create Date: 2020-08-20 23:13:35.315836

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '76f9eb571349'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True, index=True),
        sa.Column("password", sa.String, nullable=False),
        sa.Column("active", sa.Boolean, nullable=False, default=True)
    )


def downgrade():
    op.drop_table("users")
