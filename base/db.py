import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool

import settings


class BaseDatabase:
    dsn = None

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
        cls.TableBase = declarative_base(bind=cls.engine)
        cls.metadata = cls.TableBase.metadata

    def __init__(self):
        self.session = sessionmaker(bind=self.engine)
