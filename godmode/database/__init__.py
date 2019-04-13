from godmode import logging
from godmode.database.base import BaseDatabase

log = logging.getLogger(__name__)


def database(dsn: str) -> BaseDatabase:
    return BaseDatabase(dsn, connect_args={"check_same_thread": False})
