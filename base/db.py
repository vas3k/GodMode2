import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool

import settings


class BaseDatabase(object):
    dsn = None
    TableBase = declarative_base()
    metadata = TableBase.metadata

    @classmethod
    def bind(cls):
        cls.engine = sa.create_engine(
                cls.dsn,
                poolclass=QueuePool,
                pool_size=10,
                max_overflow=10,
                pool_recycle=3600,
                echo=settings.SQL_DEBUG
        )
        cls.metadata.bind = cls.engine

    def __init__(self):
        self.session = sessionmaker(bind=self.engine)
