"""add user table

Revision ID: 6593cf870d78
Revises: f7ee7de2f546
Create Date: 2022-05-15 15:42:50.477471

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6593cf870d78'
down_revision = 'f7ee7de2f546'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "users",
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('password', sa.String(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                  server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )


def downgrade():
    op.drop_table('users')
