from datetime import tzinfo
from pathlib import Path

import pytz
from PIL import Image
from pydantic_settings import BaseSettings, SettingsConfigDict

SRC_DIR = Path(__file__).resolve(strict=True).parent
REPO_DIR = SRC_DIR.parent


class Constants(BaseSettings):
    # =============== // METADATA // ===============

    title: str = "Demo App"
    description: str = "A demo app"

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

    # =============== // LINKS // ===============

    datatreehouse_url: str = "https://datatreehouse.org"
    snapscan_url: str = "https://pos.snapscan.io/qr/Ew6rBAsV"

    # =============== // GOOGLE SHEET // ===============

    G_SHEET_ID_1: str

    SCOPES: list[str] = [
        "https://www.googleapis.com/auth/spreadsheets",
    ]

    G_TYPE: str = "service_account"
    G_PROJECT_ID: str
    G_PRIVATE_KEY_ID: str
    G_PRIVATE_KEY: str
    G_CLIENT_EMAIL: str
    G_CLIENT_ID: str
    G_AUTH_URI: str = "https://accounts.google.com/o/oauth2/auth"
    G_TOKEN_URI: str = "https://oauth2.googleapis.com/token"
    G_AUTH_PROVIDER_X509_CERT_URL: str = "https://www.googleapis.com/oauth2/v1/certs"
    G_CLIENT_X509_CERT_URL: str
    G_UNIVERSE_DOMAIN: str = "googleapis.com"

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
