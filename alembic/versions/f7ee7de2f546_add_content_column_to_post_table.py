"""add content column to post table

Revision ID: f7ee7de2f546
Revises: 0fdaaadb6de7
Create Date: 2022-05-15 15:34:07.682800

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f7ee7de2f546'
down_revision = '0fdaaadb6de7'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))


def downgrade():
    # how to remove the change you want to apply
    op.drop_column("posts", column_name="content")
