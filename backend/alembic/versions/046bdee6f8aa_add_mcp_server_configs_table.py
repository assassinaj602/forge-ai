"""Add mcp_server_configs table

Revision ID: 046bdee6f8aa
Revises: 0f29774a8a23
Create Date: 2026-08-14 17:06:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = '046bdee6f8aa'
down_revision: Union[str, Sequence[str], None] = '0f29774a8a23'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.create_table('mcp_server_configs',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('user_id', sa.String(length=36), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('server_url', sa.String(length=512), nullable=False),
        sa.Column('auth_header', sa.Text(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_mcp_server_configs_user_id'), 'mcp_server_configs', ['user_id'], unique=False)

def downgrade() -> None:
    op.drop_index(op.f('ix_mcp_server_configs_user_id'), table_name='mcp_server_configs')
    op.drop_table('mcp_server_configs')
