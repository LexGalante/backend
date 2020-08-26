"""create table users

Revision ID: 685fc62404eb
Revises: 
Create Date: 2020-08-21 12:10:26.602165

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.orm import Session
from bcrypt import hashpw, gensalt


# revision identifiers, used by Alembic.
revision = '685fc62404eb'
down_revision = None
branch_labels = None
depends_on = None


def encrypt(text: str) -> str:
    to_crypt = bytes(text, 'utf-8')
    password = hashpw(to_crypt, gensalt())

    return password.decode('utf-8')


def upgrade():
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True, index=True),
        sa.Column("email", sa.String(250), unique=True, index=True, nullable=False),
        sa.Column("password", sa.String, nullable=False),
        sa.Column("active", sa.Boolean, nullable=False, default=True)
    )

    bind = op.get_bind()
    session = Session(bind=bind)
    session.execute("INSERT INTO users(email, password, active) VALUES(:email, :password, :active)", {
                    "email": "alex@iggle.com", "password": encrypt("Minh@SenhaSegura123"), "active": True})
    session.execute("INSERT INTO users(email, password, active) VALUES(:email, :password, :active)", {
                    "email": "amanda@iggle.com", "password": encrypt("Minh@SenhaSegura123"), "active": True})
    session.execute("INSERT INTO users(email, password, active) VALUES(:email, :password, :active)", {
                    "email": "nino@iggle.com", "password": encrypt("Minh@SenhaSegura123"), "active": True})
    session.execute("INSERT INTO users(email, password, active) VALUES(:email, :password, :active)", {
                    "email": "bibi@iggle.com", "password": encrypt("Minh@SenhaSegura123"), "active": True})


def downgrade():
    op.drop_table("users")
