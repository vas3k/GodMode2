import sqlalchemy as sa
from sqlalchemy.orm import relationship

from godmode.database import database
from settings import CONNECTION_STRING


vas3k_database = database(CONNECTION_STRING)


class Clickers(vas3k_database.TableBase):
    __table__ = sa.Table('clickers', vas3k_database.metadata, autoload=True)
    story = relationship('Story')


class ClickersEN(vas3k_database.TableBase):
    __table__ = sa.Table('clickers_en', vas3k_database.metadata, autoload=True)
    story = relationship('StoryEN')


class Comment(vas3k_database.TableBase):
    __table__ = sa.Table('comments', vas3k_database.metadata, autoload=True)
    story = relationship('Story')


class User(vas3k_database.TableBase):
    __table__ = sa.Table('users', vas3k_database.metadata, autoload=True)


class CommentEN(vas3k_database.TableBase):
    __table__ = sa.Table('comments_en', vas3k_database.metadata, autoload=True)
    story = relationship('StoryEN')


class Memory(vas3k_database.TableBase):
    __table__ = sa.Table('memories', vas3k_database.metadata, autoload=True)
    story = relationship('Story')


class Story(vas3k_database.TableBase):
    __table__ = sa.Table('stories', vas3k_database.metadata, autoload=True)


class StoryEN(vas3k_database.TableBase):
    __table__ = sa.Table('stories_en', vas3k_database.metadata, autoload=True)


class Pain(vas3k_database.TableBase):
    __table__ = sa.Table('pain', vas3k_database.metadata, autoload=True)


class PainAnswer(vas3k_database.TableBase):
    __table__ = sa.Table('pain_answers', vas3k_database.metadata, autoload=True)
