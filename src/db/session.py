from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from src.core import settings

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()