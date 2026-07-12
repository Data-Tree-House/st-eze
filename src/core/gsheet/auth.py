from wolpie import CredentialsInfo, GAuth, GSheets

from constants import c


def get_auth() -> GAuth:
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


def get_client(
    sheet: int = 1,
    g_auth: GAuth | None = None,
) -> GSheets:
    match sheet:
        case 1:
            sheet_id = c.G_SHEET_ID_1
        case _:
            sheet_id = c.G_SHEET_ID_1

    return GSheets(
        g_auth=g_auth or get_auth(),
        spreadsheet_id=sheet_id,
    )
