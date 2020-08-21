"""create table applications

Revision ID: 91663f1db7c5
Revises: 7cb3d8d8b071
Create Date: 2020-08-20 23:16:20.461336

"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime


# revision identifiers, used by Alembic.
revision = '91663f1db7c5'
down_revision = '7cb3d8d8b071'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "applications",
        sa.Column("id", sa.Integer, primary_key=True, index=True),
        sa.Column("name", sa.String(30), nullable=False, unique=True),
        sa.Column("real_name", sa.String(250), nullable=False),
        sa.Column("model", sa.Integer, nullable=False, default=1),
        sa.Column("description", sa.String(250), nullable=False),
        sa.Column("details", sa.String(5000), nullable=True),
        sa.Column("active", sa.Boolean, nullable=False, default=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, default=datetime.now()),
        sa.Column("created_by", sa.Integer, sa.ForeignKey("users.id")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, default=datetime.now()),
        sa.Column("updated_by", sa.Integer, sa.ForeignKey("users.id"))
    )


def downgrade():
    op.drop_table("applications")
