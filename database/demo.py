import sqlalchemy as sa
from sqlalchemy.orm import relationship

from godmode.database import database


DemoDatabase = database("sqlite:///database/demo.sqlite")


class User(DemoDatabase.TableBase):
    __table__ = sa.Table('users', DemoDatabase.metadata, autoload=True)


class Post(DemoDatabase.TableBase):
    __table__ = sa.Table('posts', DemoDatabase.metadata, autoload=True)

    user = relationship('User')
