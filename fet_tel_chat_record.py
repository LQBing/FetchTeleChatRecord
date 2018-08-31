# coding: utf-8
from sqlalchemy import Column, String, Integer, DateTime, Boolean, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from telethon import TelegramClient
from telethon.tl.types import PeerChannel, MessageActionChatJoinedByLink, MessageActionPinMessage
from telethon.tl.types import MessageActionChatAddUser, MessageActionChatDeleteUser, MessageActionChannelMigrateFrom
from settings import DBSession, StepLength, api_hash, api_id, proxy_host, proxy_port
from openpyxl import Workbook
import socks

if proxy_host and proxy_port:
    client = TelegramClient('session_name', api_id, api_hash, proxy=(socks.SOCKS5, proxy_host, proxy_port))
else:
    client = TelegramClient('session_name', api_id, api_hash)
client.start()

Base = declarative_base()

session = DBSession()
association_table = Table('association', Base.metadata,
                          Column('inviter_id', Integer, ForeignKey('user.id')),
                          Column('invitee_id', Integer, ForeignKey('user.id')),
                          Column('channel_id', Integer, ForeignKey('channel.id'))
                          )


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String)
    first_name = Column(String)
    last_name = Column(String)


class Channel(Base):
    __tablename__ = 'channels'
    id = Column(Integer, primary_key=True)
    username = Column(String)


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
    grouped_id = Column(Integer)


def save_add_user(message_id, channel_id, inviter_id, invitee_id, date, add_type):
    exist_add_user = session.query(AddUsers).filter_by(message_id=message_id, channel_id=channel_id,
                                                       inviter_id=inviter_id, invitee_id=invitee_id).first()
    if not exist_add_user:
        new_add_user = AddUsers()
        new_add_user.message_id = message_id
        new_add_user.channel_id = channel_id
        new_add_user.inviter_id = inviter_id
        new_add_user.invitee_id = invitee_id
        new_add_user.date = date
        if inviter_id == invitee_id and add_type == 'manually':
            new_add_user.add_type = 'self'
        else:
            new_add_user.add_type = add_type
        session.add(new_add_user)
        session.commit()


def save_message(message):
    print(message)
    if type(message.to_id) == PeerChannel:
        to_id = message.to_id.channel_id
        check_channel(to_id)
    else:
        to_id = message.to_id

    message_item = session.query(Message).filter_by(message_id=message.id, to_id=to_id).first()
    if not message_item:

        new_message = Message()
        if message.id:
            new_message.message_id = message.id
        if message.action:
            new_message.message_type = 'action'
            if type(message.action) == MessageActionChatJoinedByLink:
                action = 'MessageActionChatJoinedByLink'
                new_message.inviter_id = message.action.inviter_id
                save_add_user(new_message.message_id, to_id, new_message.inviter_id, message.from_id, message.date,
                              'link')
                check_user(new_message.inviter_id)
                new_message.action = action
            elif type(message.action) == MessageActionPinMessage:
                action = 'MessageActionPinMessage'
                new_message.action = action
            elif type(message.action) == MessageActionChatAddUser:
                action = 'MessageActionChatAddUser'
                new_message.action = action
                for user in message.action.users:
                    save_add_user(new_message.message_id, to_id, message.from_id, user, message.date, 'manually')
                    check_user(user)
            elif type(message.action) == MessageActionChatDeleteUser:
                action = 'MessageActionChatDeleteUser'
                new_message.action = action

            elif type(message.action) == MessageActionChannelMigrateFrom:
                action = 'MessageActionChannelMigrateFrom'
                new_message.action = action
            else:
                print(message.action)
                print(message)
                raise (AssertionError("unknown action type"))

        if to_id:
            new_message.to_id = to_id
        if message.date:
            new_message.date = message.date
        if message.message:
            new_message.message = message.message
        if message.out:
            new_message.out = message.out
        if message.mentioned:
            new_message.mentioned = message.mentioned
        if message.media_unread:
            new_message.media_unread = message.media_unread
        if message.silent:
            new_message.silent = message.silent
        if message.post:
            new_message.post = message.post
        if message.from_id:
            new_message.from_id = message.from_id
            check_user(new_message.from_id)
        if 'fwd_from' in dir(message):
            if message.fwd_from:
                new_message.fwd_from = message.fwd_from.date
        if 'via_bot_id' in dir(message):
            if message.via_bot_id:
                new_message.via_bot_id = message.via_bot_id
        if 'reply_to_msg_id' in dir(message):
            if message.reply_to_msg_id:
                new_message.reply_to_msg_id = message.reply_to_msg_id
        if 'media' in dir(message):
            if message.media:
                # new_message.media = message.media
                new_message.message_type = 'media'
        if 'reply_markup' in dir(message):
            if message.reply_markup:
                new_message.reply_markup = message.reply_markup
        if 'edit_date' in dir(message):
            if message.edit_date:
                new_message.edit_date = message.edit_date
        if 'post_author' in dir(message):
            if message.post_author:
                new_message.post_author = message.post_author
        if 'grouped_id' in dir(message):
            if message.grouped_id:
                new_message.grouped_id = message.grouped_id
        session.add(new_message)
        session.commit()


def check_user(user_id):
    exist_user = session.query(User).filter_by(id=user_id).first()
    if not exist_user:
        user = client.get_entity(user_id)
        new_user = User()
        new_user.id = user.id
        if user.username:
            new_user.username = user.username
        if user.first_name:
            new_user.first_name = user.first_name
        if user.last_name:
            new_user.last_name = user.last_name
        if user.phone:
            new_user.phone = user.phone
        session.add(new_user)
        session.commit()


def check_channel(channel_id):
    exist_channel = session.query(Channel).filter_by(id=channel_id).first()
    if not exist_channel:
        channel = client.get_entity(channel_id)
        new_channel = Channel()
        new_channel.id = channel.id
        if channel.username:
            new_channel.username = channel.username
        session.add(new_channel)
        session.commit()


def pull_channel_history(peer, top_id=0):
    if not top_id:
        history_total = client.get_messages(peer).total
        top_id = history_total // StepLength + 1
    for i in range(0, top_id):
        message_history = client.get_messages(peer, min_id=0 + i, max_id=StepLength + i * StepLength)
        for message in message_history:
            save_message(message)


def export_add_user_list_to_excel_by_id(channel_id=0, xlsx_file_name='invite_list.xlsx'):
    sql_str = "SELECT (SELECT CONCAT(IFNULL(first_name, ''), ' ', IFNULL(last_name, '')) FROM users WHERE id = add_users.inviter_id) AS inviter_name, (SELECT IFNULL(username, '') FROM users WHERE id = add_users.inviter_id) AS inviter_username, (SELECT CONCAT(IFNULL(first_name, ''), ' ', IFNULL(last_name, '')) FROM users WHERE id = add_users.invitee_id) AS invitee_name, (SELECT IFNULL(username, '') FROM users WHERE id = add_users.invitee_id) AS invitee_username, add_type, date FROM add_users"
    if channel_id:
        sql_str += " WHERE channel_id =" + str(channel_id)
        add_user_list = session.execute(sql_str).fetchall()
        if add_user_list:
            wb = Workbook()
            ws = wb.active
            ws.append(['inviter', 'invitee', 'add_type', 'date'])
            for item in add_user_list:
                item_list = list()

                if item[1]:
                    item_list.append(item[1])
                else:
                    item_list.append(item[0])
                if item[3]:
                    item_list.append(item[3])
                else:
                    item_list.append(item[2])
                item_list.append(item[4])
                item_list.append(item[5])
                print(item_list)
                ws.append(item_list)
            print('add_user_list has ' + str(len(add_user_list)) + ' records.')
            wb.save(xlsx_file_name)
            wb.close()
