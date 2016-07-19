import sqlalchemy as sa
from sqlalchemy.orm import relationship

from base.db import BaseDatabase


class DemoDatabase(BaseDatabase):
    dsn = "sqlite:///internal/demo.sqlite"


DemoDatabase.bind()


class User(DemoDatabase.TableBase):
    __table__ = sa.Table('users', DemoDatabase.metadata, autoload=True)


class Post(DemoDatabase.TableBase):
    __table__ = sa.Table('posts', DemoDatabase.metadata, autoload=True)

    user = relationship('User')
