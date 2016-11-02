import sqlalchemy as sa
from sqlalchemy.orm import relationship

from base.db import BaseDatabase
from local_settings import CONNECTION_STRING


class Vas3kDatabase(BaseDatabase):
    dsn = CONNECTION_STRING


Vas3kDatabase.bind()


class Clickers(Vas3kDatabase.TableBase):
    __table__ = sa.Table('clickers', Vas3kDatabase.metadata, autoload=True)
    story = relationship('Story')


class Comment(Vas3kDatabase.TableBase):
    __table__ = sa.Table('comments', Vas3kDatabase.metadata, autoload=True)
    story = relationship('Story')


class Memory(Vas3kDatabase.TableBase):
    __table__ = sa.Table('memories', Vas3kDatabase.metadata, autoload=True)
    story = relationship('Story')


class Story(Vas3kDatabase.TableBase):
    __table__ = sa.Table('stories', Vas3kDatabase.metadata, autoload=True)
