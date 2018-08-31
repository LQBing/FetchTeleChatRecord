# coding: utf-8
from sqlalchemy import Column, String, Integer, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String)
    first_name = Column(String)
    last_name = Column(String)


class Channel(Base):
    __tablename__ = 'channels'
    id = Column(Integer, primary_key=True)
    name = Column(String)


class AddUsers(Base):
    __tablename__ = 'add_users'

    id = Column(Integer, primary_key=True)
    message_id = Column(Integer)
    channel_id = Column(Integer)
    inviter_id = Column(Integer)
    invitee_id = Column(Integer)
    date = Column(DateTime)
    add_type = Column(String)


class Message(Base):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True)
    action = Column(String)
    inviter_id = Column(Integer)
    message_id = Column(Integer)
    message_type = Column(String)
    to_id = Column(Integer)
    date = Column(DateTime)
    message = Column(String)
    out = Column(Boolean)
    mentioned = Column(Boolean)
    media_unread = Column(Boolean)
    silent = Column(Boolean)
    post = Column(Boolean)
    from_id = Column(Integer)
    fwd_from = Column(DateTime)
    via_bot_id = Column(Integer)
    reply_to_msg_id = Column(Integer)
    media = Column(String)
    reply_markup = Column(String)
    edit_date = Column(DateTime)
    post_author = Column(String)
    grouped_id = Column(String)
