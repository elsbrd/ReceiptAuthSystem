from typing import Generator

from src.db.session import SessionLocal


def get_db_session() -> Generator[SessionLocal, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
