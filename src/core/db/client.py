from sqlalchemy import Engine
from sqlmodel import create_engine

from constants import c


def get_engine() -> Engine:
    connect_args = {}
    if "sqlite" in c.db_connection_string:
        connect_args = {"check_same_thread": False}
    return create_engine(
        c.db_connection_string,
        echo=c.db_echo,
        echo_pool=c.db_echo,
        pool_pre_ping=True,
        pool_size=5,
        pool_recycle=3600,
        connect_args=connect_args,
    )
