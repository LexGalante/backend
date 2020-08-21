"""create table environments

Revision ID: 7cb3d8d8b071
Revises: 76f9eb571349
Create Date: 2020-08-20 23:14:27.758528

"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime


# revision identifiers, used by Alembic.
revision = '7cb3d8d8b071'
down_revision = '76f9eb571349'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "environments",
        sa.Column("id", sa.Integer, primary_key=True, index=True),
        sa.Column("name", sa.String, unique=True, index=True, nullable=False),
        sa.Column("active", sa.Boolean, nullable=False, default=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, default=datetime.now()),
        sa.Column("created_by", sa.Integer, sa.ForeignKey("users.id")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, default=datetime.now()),
        sa.Column("updated_by", sa.Integer, sa.ForeignKey("users.id"))
    )


def downgrade():
    op.drop_table("environments")
