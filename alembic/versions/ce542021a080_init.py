"""init

Revision ID: ce542021a080
Revises: 
Create Date: 2024-03-28 12:17:03.899667

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ce542021a080'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("user", sa.Column('admin', sa.Boolean(), default=True, nullable=True))


def downgrade() -> None:
    op.drop_column("user", "admin")
