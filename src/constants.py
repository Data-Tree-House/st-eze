import tomllib
from datetime import tzinfo
from pathlib import Path

import pytz
from PIL import Image
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

SRC_DIR = Path(__file__).resolve(strict=True).parent
REPO_DIR = SRC_DIR.parent


def get_project_version():
    toml_path = REPO_DIR / "pyproject.toml"
    with toml_path.open("rb") as f:
        data = tomllib.load(f)
    return data.get("project", {}).get("version", "unknown")


class Constants(BaseSettings):
    # =============== // METADATA // ===============

    title: str = "eZe"
    description: str = "An application to manage your stocks with ease!"
    version: str = Field(default_factory=get_project_version)

    # =============== // LOGGING // ===============

    structured_logging: bool = True

    # =============== // Database Configurations // ===============
    # dialect[+driver]://user:password@host/dbname[?key=value..]
    # e.g. engine = create_engine("postgresql+psycopg2://scott:tiger@localhost/test")
    db_connection_string: str
    db_echo: bool = False

    default_picture: str = "https://gravatar.com/avatar/580b828f66630050b21aeaf8c20b89b3?s=400&d=mp&r=x"

    # =============== // DIRECTORIES AND PATHS // ===============

    root_dir: Path = SRC_DIR
    repo_dir: Path = REPO_DIR
    static_dir: Path = SRC_DIR / "static"

    favicon: Image.Image = Image.open(SRC_DIR / "static" / "datatreehouse.circle.png")

    logo_banner_path: str = "static/datatreehouse.banner.png"
    logo_circle_path: str = "static/datatreehouse.banner.png"
    buy_us_a_coffee_path: str = "static/buy-us-a-coffee.png"

    pages_path: str = "app/pages"

    # =============== // RABBIT // ===============

    rabbitmq_default_user: str
    rabbitmq_default_pass: str
    rmq_port: int = 5672
    rmq_host: str

    # =============== // REDIS // ===============

    redis_port: int = 6379
    redis_host: str = "redis"

    # =============== // LINKS // ===============

    datatreehouse_url: str = "https://datatreehouse.org"
    snapscan_url: str = "https://pos.snapscan.io/qr/Ew6rBAsV"

    # =============== // GOOGLE SHEET // ===============

    g_worker_ids: list[str]
    g_worker_pool_timeout: float = 300  # seconds

    g_integration_test_sheet_id: str = ""

    scopes: list[str] = [
        "https://www.googleapis.com/auth/spreadsheets",
    ]

    g_type: str = "service_account"
    g_project_id: str
    g_private_key_id: str
    g_private_key: str
    g_client_email: str
    g_client_id: str
    g_auth_uri: str = "https://accounts.google.com/o/oauth2/auth"
    g_token_uri: str = "https://oauth2.googleapis.com/token"
    g_auth_provider_x509_cert_url: str = "https://www.googleapis.com/oauth2/v1/certs"
    g_client_x509_cert_url: str
    g_universe_domain: str = "googleapis.com"

    # =============== // UMAMI // ===============

    umami_website_id: str
    umami_host: str

    tz: tzinfo = pytz.timezone("Africa/Johannesburg")

    model_config = SettingsConfigDict(
        env_file=str(REPO_DIR / ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )


c = Constants()  # type: ignore
