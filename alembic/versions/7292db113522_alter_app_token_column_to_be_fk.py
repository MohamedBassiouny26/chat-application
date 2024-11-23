"""alter app_token column to be fk

Revision ID: 7292db113522
Revises: 7fbacf922393
Create Date: 2024-11-23 00:12:58.416895

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7292db113522'
down_revision: Union[str, None] = '7fbacf922393'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('app_token', table_name='chats')
    op.create_foreign_key(None, 'chats', 'applications', ['app_token'], ['token'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'chats', type_='foreignkey')
    op.create_index('app_token', 'chats', ['app_token'], unique=True)
    # ### end Alembic commands ###
