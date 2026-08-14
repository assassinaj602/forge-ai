"""Add semantic_cache_entries table

Revision ID: eed441c63d1c
Revises: 046bdee6f8aa
Create Date: 2026-08-14 17:45:50.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = 'eed441c63d1c'
down_revision: Union[str, Sequence[str], None] = '046bdee6f8aa'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.create_table('semantic_cache_entries',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('user_id', sa.String(length=36), nullable=False),
        sa.Column('prompt', sa.Text(), nullable=False),
        sa.Column('response_content', sa.Text(), nullable=False),
        sa.Column('provider', sa.String(length=50), nullable=False),
        sa.Column('model', sa.String(length=100), nullable=False),
        sa.Column('hit_count', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_semantic_cache_entries_user_id'), 'semantic_cache_entries', ['user_id'], unique=False)

def downgrade() -> None:
    op.drop_index(op.f('ix_semantic_cache_entries_user_id'), table_name='semantic_cache_entries')
    op.drop_table('semantic_cache_entries')
