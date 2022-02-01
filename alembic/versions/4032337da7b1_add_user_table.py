"""add user table

Revision ID: 4032337da7b1
Revises: 3d34c884d848
Create Date: 2022-02-01 15:55:40.359605

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4032337da7b1'
down_revision = '3d34c884d848'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("USERS", sa.Column("ID", sa.Integer(), nullable=False),
                    sa.Column("EMAIL", sa.String(), nullable=False),
                    sa.Column("PASSWORD", sa.String(), nullable=False),
                    sa.Column("CREATED_AT", sa.TIMESTAMP(timezone=True),server_default=sa.text('now()'),
                              nullable=False),
                    sa.PrimaryKeyConstraint('ID'),
                    sa.UniqueConstraint('EMAIL'))
    pass


def downgrade():
    op.drop_table("USERS")
    pass
