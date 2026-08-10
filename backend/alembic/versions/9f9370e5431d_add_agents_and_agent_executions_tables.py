"""Add agents and agent_executions tables

Revision ID: 9f9370e5431d
Revises: 30e969cbd9d4
Create Date: 2026-08-11 01:33:55.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = '9f9370e5431d'
down_revision: Union[str, Sequence[str], None] = '30e969cbd9d4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.create_table('agents',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('user_id', sa.String(length=36), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('system_instructions', sa.Text(), nullable=False),
        sa.Column('model', sa.String(length=100), nullable=False),
        sa.Column('provider', sa.String(length=50), nullable=False),
        sa.Column('max_iterations', sa.Integer(), nullable=False),
        sa.Column('temperature', sa.Float(), nullable=False),
        sa.Column('tools', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_agents_user_id'), 'agents', ['user_id'], unique=False)

    op.create_table('agent_executions',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('agent_id', sa.String(length=36), nullable=False),
        sa.Column('user_id', sa.String(length=36), nullable=False),
        sa.Column('task', sa.Text(), nullable=False),
        sa.Column('status', sa.String(length=50), nullable=False),
        sa.Column('final_answer', sa.Text(), nullable=True),
        sa.Column('iteration_count', sa.Integer(), nullable=False),
        sa.Column('steps_log', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('completed_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['agent_id'], ['agents.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_agent_executions_agent_id'), 'agent_executions', ['agent_id'], unique=False)
    op.create_index(op.f('ix_agent_executions_user_id'), 'agent_executions', ['user_id'], unique=False)

def downgrade() -> None:
    op.drop_index(op.f('ix_agent_executions_user_id'), table_name='agent_executions')
    op.drop_index(op.f('ix_agent_executions_agent_id'), table_name='agent_executions')
    op.drop_table('agent_executions')
    op.drop_index(op.f('ix_agents_user_id'), table_name='agents')
    op.drop_table('agents')
