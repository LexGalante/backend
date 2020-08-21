"""create table application_features

Revision ID: 719115ad2dcf
Revises: 65612885ab31
Create Date: 2020-08-20 23:22:15.639304

"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime


# revision identifiers, used by Alembic.
revision = '719115ad2dcf'
down_revision = '65612885ab31'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "application_features",
        sa.Column("id", sa.Integer, primary_key=True, index=True),
        sa.Column("application_id", sa.Integer, sa.ForeignKey("applications.id")),
        sa.Column("enviroment_id", sa.Integer, sa.ForeignKey("application_environments.id")),
        sa.Column("name", sa.String(250), nullable=False),
        sa.Column("enable", sa.Boolean, nullable=False, default=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, default=datetime.now()),
        sa.Column("created_by", sa.Integer, sa.ForeignKey("users.id")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, default=datetime.now()),
        sa.Column("updated_by", sa.Integer, sa.ForeignKey("users.id"))
    )


def downgrade():
    op.drop_table("application_features")
