from sqlalchemy import Column, String, Boolean, MetaData, UniqueConstraint, Enum, DateTime, ForeignKey, Text, func
from sqlalchemy.dialects.postgresql import UUID
import uuid
import enum
from sqlalchemy.orm import declarative_base


convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

metadata = MetaData(naming_convention=convention)
Base = declarative_base(metadata=metadata)


class UserRole(str, enum.Enum):
    USER = "user"
    ADMIN = "admin"


class User(Base):
    __tablename__ = 'users'

    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.USER, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)


class Category(Base):
    __tablename__ = 'categories'
    __table_args__ = (
        UniqueConstraint('name', name='uq_categories_name'),
    )

    category_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    description = Column(String(500), nullable=False)


class Article(Base):
    __tablename__ = 'articles'

    article_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    text = Column(Text, nullable=False)
    category_id = Column(UUID(as_uuid=True), ForeignKey('categories.category_id'), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    is_deleted = Column(Boolean, nullable=False, default=False)
