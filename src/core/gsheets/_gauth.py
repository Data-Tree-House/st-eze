import logging
import os
from pathlib import Path
from typing import Any

from google.oauth2 import service_account
from pydantic import BaseModel


class CredentialsInfo(BaseModel):
    type: str = "service_account"
    project_id: str
    private_key_id: str
    private_key: str
    client_email: str
    client_id: str
    auth_uri: str
    token_uri: str
    auth_provider_x509_cert_url: str
    client_x509_cert_url: str
    universe_domain: str


def credentials_from_env(prefix: str = "G") -> CredentialsInfo:
    """Load Google service account credentials from environment variables.

    GFinanceArgs:
        prefix: The prefix for environment variable names. Default is "G".

    Returns:
        A CredentialsInfo object containing the credentials.

    Example:
        ```python
        # Set environment variables like G_PROJECT_ID, G_PRIVATE_KEY, etc.
        creds = credentials_from_env(prefix="G")
        ```
    """
    env_vars = {
        "type": "service_account",
        "project_id": "",
        "private_key_id": "",
        "private_key": "",
        "client_email": "",
        "client_id": "",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "",
        "universe_domain": "googleapis.com",
    }

    for key, default_value in env_vars.items():
        env_var_name = f"{prefix}_{key.upper()}" if prefix else key.upper()
        env_var_value = os.getenv(env_var_name, default_value) if default_value else os.getenv(env_var_name)
        if env_var_value is not None:
            env_vars[key] = env_var_value

    return CredentialsInfo(**env_vars)


class GAuth:
    """Google authentication handler for service accounts.

    This class manages Google service account credentials and provides
    authentication for Google API services.

    GFinanceArgs:
        logger: Optional logger instance for logging.
        credentials_path: Path to the service account JSON file.
        credentials_info: CredentialsInfo object with service account details.
        scopes: List of OAuth scopes to request.
        **kwargs: Additional keyword arguments passed to credentials.

    Raises:
        ValueError: If neither credentials_info nor credentials_path is provided.

    Example:
        ```python
        from pathlib import Path
        from core.gsheets.gsheets import GAuth

        # Using credentials file
        auth = GAuth(credentials_path=Path("service-account.json"))

        # Using credentials from environment
        from core.gsheets.gsheets._gauth import credentials_from_env
        auth = GAuth(credentials_info=credentials_from_env())
        ```
    """

    def __init__(
        self,
        logger: logging.Logger | None = None,
        credentials_path: Path | None = None,
        credentials_info: CredentialsInfo | None = None,
        scopes: list[str] | None = None,
        **kwargs: Any,
    ) -> None:
        self._logger = logger or logging.getLogger(__name__)

        if credentials_info is None and credentials_path is None:
            raise ValueError("Either credentials_info or credentials_path must be provided.")

        if scopes is not None:
            kwargs["scopes"] = scopes

        if credentials_path is not None and credentials_path.exists():
            self._logger.debug(f"Using credentials from {credentials_path}")
            self.credentials = service_account.Credentials.from_service_account_file(
                str(credentials_path),
                **kwargs,
            )

        if credentials_info is not None:
            self._logger.debug("Using credentials from provided info")
            self.credentials = service_account.Credentials.from_service_account_info(
                info=credentials_info.model_dump(),
                **kwargs,
            )
