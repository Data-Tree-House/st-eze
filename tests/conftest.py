import tempfile
from pathlib import Path
from typing import TYPE_CHECKING

import pytest
from wolpie import CredentialsInfo, GAuth

from constants import c

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
            type=c.G_TYPE,
            project_id=c.G_PROJECT_ID,
            private_key_id=c.G_PRIVATE_KEY_ID,
            private_key=c.G_PRIVATE_KEY,
            client_email=c.G_CLIENT_EMAIL,
            client_id=c.G_CLIENT_ID,
            auth_uri=c.G_AUTH_URI,
            token_uri=c.G_TOKEN_URI,
            auth_provider_x509_cert_url=c.G_AUTH_PROVIDER_X509_CERT_URL,
            client_x509_cert_url=c.G_CLIENT_X509_CERT_URL,
            universe_domain=c.G_UNIVERSE_DOMAIN,
        ),
        scopes=c.SCOPES,
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
