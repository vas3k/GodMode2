import sqlalchemy as sa
from sqlalchemy.orm import relationship

from base.db import BaseDatabase
from settings import CONNECTION_STRING


class Vas3kDatabase(BaseDatabase):
    dsn = CONNECTION_STRING


Vas3kDatabase.bind()


class Clickers(Vas3kDatabase.TableBase):
    __table__ = sa.Table('clickers', Vas3kDatabase.metadata, autoload=True)
    story = relationship('Story')


class ClickersEN(Vas3kDatabase.TableBase):
    __table__ = sa.Table('clickers_en', Vas3kDatabase.metadata, autoload=True)
    story = relationship('StoryEN')


class Comment(Vas3kDatabase.TableBase):
    __table__ = sa.Table('comments', Vas3kDatabase.metadata, autoload=True)
    story = relationship('Story')


class CommentEN(Vas3kDatabase.TableBase):
    __table__ = sa.Table('comments_en', Vas3kDatabase.metadata, autoload=True)
    story = relationship('StoryEN')


class Memory(Vas3kDatabase.TableBase):
    __table__ = sa.Table('memories', Vas3kDatabase.metadata, autoload=True)
    story = relationship('Story')


class Story(Vas3kDatabase.TableBase):
    __table__ = sa.Table('stories', Vas3kDatabase.metadata, autoload=True)


class StoryEN(Vas3kDatabase.TableBase):
    __table__ = sa.Table('stories_en', Vas3kDatabase.metadata, autoload=True)


class Pain(Vas3kDatabase.TableBase):
    __table__ = sa.Table('pain', Vas3kDatabase.metadata, autoload=True)
