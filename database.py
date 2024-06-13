import os
from sqlalchemy import create_engine

from sqlalchemy.orm import sessionmaker, declarative_base


# Correct database URL with 'postgresql' dialect
SQLALCHEMY_DATABASE_URL = "postgresql://default:i14qYZSsmfld@ep-icy-dawn-a1xdt1o8.ap-southeast-1.aws.neon.tech:5432/verceldb?sslmode=require"
# Create the SQLAlchemy engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for our ORM models
Base = declarative_base()

