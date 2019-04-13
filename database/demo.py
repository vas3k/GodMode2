import sqlalchemy as sa
from sqlalchemy.orm import relationship

from godmode.database import database


demo_database = database("sqlite:///database/demo.sqlite", connect_args={"check_same_thread": False})


class User(demo_database.TableBase):
    __table__ = sa.Table('users', demo_database.metadata, autoload=True)


class Post(demo_database.TableBase):
    __table__ = sa.Table('posts', demo_database.metadata, autoload=True)

    user = relationship('User')
