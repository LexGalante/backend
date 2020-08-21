"""create table environments

Revision ID: 7cb3d8d8b071
Revises: 76f9eb571349
Create Date: 2020-08-20 23:14:27.758528

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.orm import Session

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
