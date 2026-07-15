import tempfile
from pathlib import Path
from typing import TYPE_CHECKING

import pytest

from constants import c
from core.gsheets import CredentialsInfo, GAuth

if TYPE_CHECKING:
    from collections.abc import Generator


@pytest.fixture
def temp_dir() -> Generator[Path]:
    """Create a temporary directory that's cleaned up after the test."""
    with tempfile.TemporaryDirectory(
        dir=Path(__file__).parent / "tmp",
    ) as tmpdir:
        yield Path(tmpdir)


@pytest.fixture(scope="session")
def g_auth() -> GAuth:
    return GAuth(
        credentials_info=CredentialsInfo(
            type=c.g_type,
            project_id=c.g_project_id,
            private_key_id=c.g_private_key_id,
            private_key=c.g_private_key,
            client_email=c.g_client_email,
            client_id=c.g_client_id,
            auth_uri=c.g_auth_uri,
            token_uri=c.g_token_uri,
            auth_provider_x509_cert_url=c.g_auth_provider_x509_cert_url,
            client_x509_cert_url=c.g_client_x509_cert_url,
            universe_domain=c.g_universe_domain,
        ),
        scopes=c.scopes,
    )


# @pytest.fixture(scope="class")
# def mock_engine() -> Generator[Engine]:
#     """Create a fresh in-memory SQLite database for each test."""
#     engine = create_engine("sqlite:///:memory:", echo=True)
#     crud.create_all_tables(engine)

#     yield engine

#     # However, there are many cases where it is desirable that all connection resources referred to by the Engine be
#     # completely closed out. It's generally not a good idea to rely on Python garbage collection for this to occur for
#     # these cases; instead, the Engine can be explicitly disposed using the Engine.dispose() method.
#     # ref: https://docs.sqlalchemy.org/en/21/core/connections.html
#     engine.dispose()


# @pytest.fixture(scope="module")
# def pg_engine() -> Generator[Engine]:
#     with PostgresContainer("postgres:18-alpine") as postgres:
#         engine = create_engine(postgres.get_connection_url(), echo=True)
#         crud.create_all_tables(engine)
#         yield engine
#         engine.dispose()
