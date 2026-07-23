from collections.abc import Generator

from sqlmodel import Session

from core.db import get_engine


def get_session() -> Generator[Session]:
    with Session(get_engine()) as session:
        try:
            yield session
            session.commit()  # just in case
        except Exception:
            session.rollback()
            raise
