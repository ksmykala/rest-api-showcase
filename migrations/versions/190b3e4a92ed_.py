"""Add email column to users

Revision ID: 190b3e4a92ed
Revises: e04cb14d073f
Create Date: 2025-04-01 07:26:16.970468

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '190b3e4a92ed'
down_revision = 'e04cb14d073f'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('email', sa.String(), nullable=True))
        batch_op.create_unique_constraint('email', ['email'])


def downgrade():
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_constraint('email', type_='unique')
        batch_op.drop_column('email')
