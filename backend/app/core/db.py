from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Text, DateTime, Enum, Index, Boolean, ForeignKey
from datetime import datetime, timezone
from app.config import settings
import logging

logger = logging.getLogger(__name__)

Base = declarative_base()

# Database engine
engine = create_async_engine(
    settings.database_url,
    echo=settings.environment == "development",
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20
)

# Session factory
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)


# Database Models
class PromptRecord(Base):
    """
    The prompts table in the database
    """
    __tablename__ = settings.db_prompts_table_name

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    prompt = Column(Text, nullable=False)
    project_name = Column(String(100), nullable=False, index=True)
    user_id = Column(String(100), nullable=False, index=True)
    company_id = Column(String(100), nullable=False, index=True)
    idempotency_key = Column(String(100), nullable=False, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False, index=False)

    # Composite indexes for common queries
    __table_args__ = (
        Index('idx_project_user', 'project_name', 'user_id'),
        Index('idx_user_created', 'user_id', 'created_at'),
        Index('idx_idempotency_key', 'idempotency_key', 'idempotency_key'),
        Index('idx_company_id', 'company_id', 'company_id')
    )


class UsersRecord(Base):
    """
    The users table in the database
    """
    __tablename__ = settings.db_users_table_name

    user_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(100), nullable=False, index=True)
    email = Column(String(100), nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)
    last_active = Column(DateTime, default=datetime.now(timezone.utc))
    company = Column(String(100), nullable=True, index=True)

    # Composite indexes for common queries
    __table_args__ = (
        Index('idx_user_id', 'user_id', 'user_id'),
        Index('idx_email', 'email', 'email'),
        Index('idx_company', 'company', 'company')
    )


class ProjectsRecord(Base):
    """
    The projects table in the database
    """
    __tablename__ = settings.db_projects_table_name

    project_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    project_name = Column(String(100), nullable=False, index=True)
    description = Column(Text, nullable=True, index=False)
    company_id = Column(String(100), nullable=True, index=True)
    created_by = Column(String(100), nullable=False, index=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc), nullable=False, index=False)
    is_active = Column(Boolean, default=True, nullable=False, index=False)

    # Composite indexes for common queries
    __table_args__ = (
        Index('idx_project_name', 'project_name', 'project_name'),
        Index('idx_company_id', 'company_id', 'company_id'),
    )


"""
class PromptRunningStatus(Base):
    execution_status = Column(
        Enum("success", "failed", "pending", name="execution_status_enum"),
        nullable=False,
        default="pending"
    )
"""


# Dependency for database sessions
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


async def init_db():
    """Initialize database - create tables if they don't exist"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database tables created/verified successfully")
