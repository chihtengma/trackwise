"""Add social authentication fields to User model

Revision ID: add_social_auth_001
Revises:
Create Date: 2025-11-02 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'add_social_auth_001'
down_revision: Union[str, None] = 'be45eb4da5f1'  # After saved_routes migration
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add social authentication columns to users table
    op.add_column('users', sa.Column('google_id', sa.String(255), nullable=True))
    op.add_column('users', sa.Column('apple_id', sa.String(255), nullable=True))
    op.add_column('users', sa.Column('auth_provider', sa.String(50), nullable=True))
    op.add_column('users', sa.Column('email_verified', sa.Boolean(), nullable=False, server_default='false'))
    op.add_column('users', sa.Column('profile_picture', sa.Text(), nullable=True))

    # Create unique indexes for social provider IDs
    op.create_index('ix_users_google_id', 'users', ['google_id'], unique=True)
    op.create_index('ix_users_apple_id', 'users', ['apple_id'], unique=True)

    # Make hashed_password nullable for social auth users
    op.alter_column('users', 'hashed_password',
                    existing_type=sa.String(255),
                    nullable=True)


def downgrade() -> None:
    # Remove indexes
    op.drop_index('ix_users_google_id', table_name='users')
    op.drop_index('ix_users_apple_id', table_name='users')

    # Remove social authentication columns
    op.drop_column('users', 'profile_picture')
    op.drop_column('users', 'email_verified')
    op.drop_column('users', 'auth_provider')
    op.drop_column('users', 'apple_id')
    op.drop_column('users', 'google_id')

    # Make hashed_password non-nullable again
    op.alter_column('users', 'hashed_password',
                    existing_type=sa.String(255),
                    nullable=False)