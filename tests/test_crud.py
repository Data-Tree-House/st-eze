import pytest
from sqlalchemy import Engine
from sqlmodel import Session

from core.db import crud, m


class TestStock:
    @pytest.fixture(autouse=True)
    def setup(self, mock_engine: Engine):
        pass

    def test_new_stock_with_minimal_info(self, mock_engine: Engine):
        with Session(mock_engine) as session:
            new_stock: m.Stock = crud.create_stock(
                session=session,
                ticker="GOOGL",
                exchange="NASDAQ",
            )
