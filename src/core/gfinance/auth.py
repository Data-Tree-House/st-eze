from functools import lru_cache

from constants import c
from core.gsheets import CredentialsInfo, GAuth, GSheets


@lru_cache
def get_auth() -> GAuth:
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


def get_client(
    sheet_id: str,
    g_auth: GAuth | None = None,
) -> GSheets:
    return GSheets(
        g_auth=g_auth or get_auth(),
        spreadsheet_id=sheet_id,
    )
