from datetime import datetime

from sqlalchemy import Integer, Column, DateTime, String, ForeignKey

import settings
from godmode.database import database


godmode_database = database(settings.APP_DSN, connect_args={"check_same_thread": False})


class UsersTable(godmode_database.TableBase):
    __tablename__ = "gm_users"

    id = Column(Integer, primary_key=True)
    login = Column(String(32), unique=True)
    password = Column(String(64))
    acl = Column(String(16))
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)


class SessionsTable(godmode_database.TableBase):
    __tablename__ = "gm_sessions"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("gm_users.id"))
    token = Column(String(32))
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)


class LogTable(godmode_database.TableBase):
    __tablename__ = "gm_log"

    id = Column(Integer, primary_key=True)
    user = Column(String(32))
    model = Column(String(64))
    action = Column(String(512))
    ids = Column(String(4096))
    details = Column(String(512))
    reason = Column(String(64))
    created_at = Column(DateTime, default=datetime.now)
