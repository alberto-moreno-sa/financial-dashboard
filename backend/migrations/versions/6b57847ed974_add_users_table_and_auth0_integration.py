"""Add users table and auth0 integration

Revision ID: 6b57847ed974
Revises: d6c2d9c812eb
Create Date: 2025-12-26 17:13:29.405808

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '6b57847ed974'
down_revision: Union[str, None] = 'd6c2d9c812eb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Drop old tables first (if they exist)
    op.execute("DROP TABLE IF EXISTS positions CASCADE")
    op.execute("DROP TABLE IF EXISTS portfolios CASCADE")

    # Create users table
    op.create_table('users',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('auth0_id', sa.String(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=True),
        sa.Column('picture', sa.String(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True, server_default='true'),
        sa.Column('email_verified', sa.Boolean(), nullable=True, server_default='false'),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.Column('last_login_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_auth0_id'), 'users', ['auth0_id'], unique=True)
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)

    # Create portfolios table (with user_id foreign key)
    op.create_table('portfolios',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('user_id', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=False, server_default='Mi Portafolio'),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('currency', sa.String(), nullable=False, server_default='MXN'),
        sa.Column('total_net_worth', sa.Numeric(precision=15, scale=2), nullable=False, server_default='0.00'),
        sa.Column('cash_balance', sa.Numeric(precision=15, scale=2), nullable=False, server_default='0.00'),
        sa.Column('invested_value', sa.Numeric(precision=15, scale=2), nullable=False, server_default='0.00'),
        sa.Column('is_active', sa.Boolean(), nullable=True, server_default='true'),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_portfolios_user_id'), 'portfolios', ['user_id'], unique=False)

    # Create positions table (with portfolio_id foreign key)
    op.create_table('positions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('portfolio_id', sa.String(), nullable=False),
        sa.Column('ticker', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('asset_type', sa.String(), nullable=True, server_default='Stock'),
        sa.Column('quantity', sa.Numeric(precision=15, scale=4), nullable=False),
        sa.Column('avg_cost', sa.Numeric(precision=15, scale=2), nullable=False),
        sa.Column('current_price', sa.Numeric(precision=15, scale=2), nullable=False),
        sa.Column('market_value', sa.Numeric(precision=15, scale=2), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['portfolio_id'], ['portfolios.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_positions_id'), 'positions', ['id'], unique=False)
    op.create_index(op.f('ix_positions_portfolio_id'), 'positions', ['portfolio_id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_positions_portfolio_id'), table_name='positions')
    op.drop_index(op.f('ix_positions_id'), table_name='positions')
    op.drop_table('positions')
    op.drop_index(op.f('ix_portfolios_user_id'), table_name='portfolios')
    op.drop_table('portfolios')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_index(op.f('ix_users_auth0_id'), table_name='users')
    op.drop_table('users')
