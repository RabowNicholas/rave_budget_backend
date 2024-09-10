# database.py
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "postgresql+asyncpg://postgres:admin@/cloudsql/ravebudget:us-central1:rave-budget/postgres"
# Create the async engine
engine = create_async_engine(DATABASE_URL, echo=True)

# Create a sessionmaker instance
SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, class_=AsyncSession
)

# Base class for models
Base = declarative_base()
