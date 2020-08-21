"""create table application_users

Revision ID: 1f94bf3b665e
Revises: 91663f1db7c5
Create Date: 2020-08-20 23:17:22.422958

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.schema import Sequence, CreateSequence


# revision identifiers, used by Alembic.
revision = '1f94bf3b665e'
down_revision = '91663f1db7c5'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "application_users",
        sa.Column("id", sa.Integer, index=True),
        sa.Column("application_id", sa.Integer, sa.ForeignKey("applications.id")),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id"))
    )

    op.create_primary_key(
        "application_users_pk",
        "application_users",
        ["id", "application_id", "user_id"]
    )

    op.execute(CreateSequence(Sequence('application_users_id_seq')))
    op.alter_column(
        "application_users",
        "id",
        nullable=False, server_default=sa.text("nextval('application_users_id_seq'::regclass)"))


def downgrade():
    op.drop_table("application_users")
