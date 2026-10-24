"""add search_vector to articles

Revision ID: f9d377da3f22
Revises: b1e7e74608a7
Create Date: ...

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'f9d377da3f22'               # <-- ЭТА СТРОКА
down_revision: Union[str, Sequence[str], None] = 'b1e7e74608a7'  # <-- И ЭТА
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.add_column('articles', sa.Column('search_vector', postgresql.TSVECTOR(), nullable=True))


    op.execute("""
        CREATE FUNCTION articles_search_trigger() RETURNS trigger AS $$
        begin
          new.search_vector :=
            setweight(to_tsvector('russian', coalesce(new.title,'')), 'A') ||
            setweight(to_tsvector('russian', coalesce(new.text,'')), 'B');
          return new;
        end
        $$ LANGUAGE plpgsql;
    """)


    op.execute("""
        CREATE TRIGGER tsvectorupdate BEFORE INSERT OR UPDATE
        ON articles FOR EACH ROW EXECUTE FUNCTION articles_search_trigger();
    """)

    # 4. Создаем GIN-индекс для быстрого поиска
    op.create_index('idx_articles_search_vector', 'articles', ['search_vector'], unique=False, postgresql_using='gin')


    op.execute("""
        UPDATE articles SET search_vector = 
            setweight(to_tsvector('russian', coalesce(title,'')), 'A') ||
            setweight(to_tsvector('russian', coalesce(text,'')), 'B');
    """)


def downgrade() -> None:
    """Downgrade schema."""
    # Удаляем триггер и функцию
    op.execute("DROP TRIGGER IF EXISTS tsvectorupdate ON articles;")
    op.execute("DROP FUNCTION IF EXISTS articles_search_trigger();")

    # Удаляем индекс
    op.drop_index('idx_articles_search_vector', table_name='articles')

    # Удаляем колонку
    op.drop_column('articles', 'search_vector')