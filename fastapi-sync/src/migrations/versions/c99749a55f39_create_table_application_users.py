"""create table application_users

Revision ID: c99749a55f39
Revises: 6cbae6678e5c
Create Date: 2020-08-21 12:25:08.375647

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.schema import Sequence, CreateSequence
from sqlalchemy.orm import Session


# revision identifiers, used by Alembic.
revision = 'c99749a55f39'
down_revision = '6cbae6678e5c'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "application_users",
        sa.Column("id", sa.Integer, primary_key=True, index=True),
        sa.Column("application_id", sa.Integer, sa.ForeignKey("applications.id")),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id"))
    )

    op.create_unique_constraint(
        "application_users_un",
        "application_users",
        ["application_id", "user_id"],
        schema="public"
    )

    bind = op.get_bind()
    session = Session(bind=bind)
    session.execute(
        "INSERT INTO application_users(application_id, user_id) VALUES(:application_id, :user_id)",
        {"application_id": 1, "user_id": 1})
    session.execute(
        "INSERT INTO application_users(application_id, user_id) VALUES(:application_id, :user_id)",
        {"application_id": 2, "user_id": 1})
    session.execute(
        "INSERT INTO application_users(application_id, user_id) VALUES(:application_id, :user_id)",
        {"application_id": 3, "user_id": 1})
    session.execute(
        "INSERT INTO application_users(application_id, user_id) VALUES(:application_id, :user_id)",
        {"application_id": 1, "user_id": 2})
    session.execute(
        "INSERT INTO application_users(application_id, user_id) VALUES(:application_id, :user_id)",
        {"application_id": 2, "user_id": 2})


def downgrade():
    op.drop_table("application_users")
