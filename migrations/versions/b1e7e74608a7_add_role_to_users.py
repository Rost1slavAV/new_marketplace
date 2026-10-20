"""add role to users

Revision ID: b1e7e74608a7
Revises: b07b3b15b1b2
Create Date: ...

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b1e7e74608a7'
down_revision: Union[str, Sequence[str], None] = 'b07b3b15b1b2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    userrole = sa.Enum('USER', 'ADMIN', name='userrole')
    userrole.create(op.get_bind(), checkfirst=True)

    op.add_column(
        'users',
        sa.Column('role', userrole, nullable=False, server_default='USER'),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('users', 'role')
    sa.Enum(name='userrole').drop(op.get_bind(), checkfirst=True)