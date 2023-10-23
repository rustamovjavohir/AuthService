import logging
import sys
from typing import List

from databases import DatabaseURL
from loguru import logger
from starlette.config import Config
from starlette.datastructures import CommaSeparatedStrings, Secret

from app.core.logging import InterceptHandler

API_PREFIX = '/api'

VERSION = '0.0.1'

config = Config('.env')

DEBUG: bool = config.get("DEBUG", cast=bool, default=False)

DATABASE_URL: DatabaseURL = config.get("DB_CONNECTION", cast=DatabaseURL)
MAX_CONNECTIONS_COUNT: int = config("MAX_CONNECTIONS_COUNT", cast=int, default=10)
MIN_CONNECTIONS_COUNT: int = config("MIN_CONNECTIONS_COUNT", cast=int, default=10)

SECRET_KEY: Secret = config.get("SECRET_KEY", cast=Secret)
PROJECT_NAME: str = config.get("PROJECT_NAME", default="Auth service")

ALLOWED_HOSTS: List[str] = config.get("ALLOWED_HOSTS", cast=CommaSeparatedStrings, default='')

# logging configuration

LOGGING_LEVEL = logging.DEBUG if DEBUG else logging.INFO
logging.basicConfig(
    handlers=[InterceptHandler(level=LOGGING_LEVEL)],
    level=LOGGING_LEVEL
)

logger.configure(handlers=[{"sink": sys.stderr, "level": LOGGING_LEVEL}])

# JWT configuration
JWT_TOKEN_PREFIX = "Bearer"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # one week
ALGORITHM = "HS256"
