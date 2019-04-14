import hashlib

import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool

import settings


class BaseDatabase:
    def __init__(self, dsn: str, **kwargs):
        self.dsn = dsn
        self.engine = sa.create_engine(
            dsn,
            poolclass=QueuePool,
            pool_size=10,
            max_overflow=10,
            pool_recycle=3600,
            echo=settings.SQL_DEBUG,
            **kwargs
        )
        self.TableBase = declarative_base(bind=self.engine)  # pylint: disable=invalid-name
        self.metadata = self.TableBase.metadata
        self.session = sessionmaker(bind=self.engine)()
        self.hash = hashlib.sha256(self.dsn.encode()).hexdigest()
