from sqlalchemy import Engine
from sqlmodel import Field, SQLModel


class Hero(SQLModel, table=True):
    __tablename__ = "hero_table"
    __table_args__ = {"extend_existing": True}

    id: int | None = Field(default=None, primary_key=True)
    name: str
    secret_name: str
    age: int | None = None


def create_all(engine: Engine):
    SQLModel.metadata.create_all(
        engine,
        checkfirst=True,
    )
