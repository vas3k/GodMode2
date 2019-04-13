from godmode import logging
from godmode.database.base import BaseDatabase

log = logging.getLogger(__name__)


def database(dsn: str, **kwargs) -> BaseDatabase:
    return BaseDatabase(dsn, **kwargs)
