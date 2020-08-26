"""create table environments

Revision ID: b15b0aa87418
Revises: 685fc62404eb
Create Date: 2020-08-21 12:11:27.556501

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.orm import Session


# revision identifiers, used by Alembic.
revision = 'b15b0aa87418'
down_revision = '685fc62404eb'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "environments",
        sa.Column("id", sa.Integer, primary_key=True, index=True),
        sa.Column("name", sa.String, unique=True, index=True, nullable=False),
        sa.Column("description", sa.String, nullable=False),
        sa.Column("active", sa.Boolean, nullable=False, default=True)
    )

    bind = op.get_bind()
    session = Session(bind=bind)
    session.execute("INSERT INTO environments(name, description, active) VALUES(:name, :description, :active)", {
                    "name": "dev", "description": "Development", "active": True})
    session.execute("INSERT INTO environments(name, description, active) VALUES(:name, :description, :active)", {
                    "name": "tes", "description": "Testing", "active": True})
    session.execute("INSERT INTO environments(name, description, active) VALUES(:name, :description, :active)", {
                    "name": "hml", "description": "Homologation", "active": True})
    session.execute("INSERT INTO environments(name, description, active) VALUES(:name, :description, :active)", {
                    "name": "prd", "description": "Production", "active": True})


def downgrade():
    op.drop_table("environments")
