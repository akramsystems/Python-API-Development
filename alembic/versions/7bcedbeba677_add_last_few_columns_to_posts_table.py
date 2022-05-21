"""add last few columns to posts table

Revision ID: 7bcedbeba677
Revises: 6675e48acfe5
Create Date: 2022-05-21 15:16:11.648188

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7bcedbeba677'
down_revision = '6675e48acfe5'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts",
                  sa.Column("published", sa.Boolean(), nullable=False, server_default='TRUE'))
    op.add_column("posts",
                  sa.Column("created_at",
                            sa.TIMESTAMP(timezone=True),
                            nullable=False,
                            server_default=sa.text("NOW()")))


def downgrade():
    op.drop_column("posts", "published")
    op.drop_column("posts", "created_at")
