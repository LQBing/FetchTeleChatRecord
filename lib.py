# coding: utf-8\
from sqlalchemy.ext.declarative import declarative_base
from telethon import TelegramClient
from telethon.tl.types import PeerChannel, MessageActionChatJoinedByLink, MessageActionPinMessage
from telethon.tl.types import MessageActionChatAddUser, MessageActionChatDeleteUser, MessageActionChannelMigrateFrom
from settings import DBSession, StepLength, api_hash, api_id, proxy_host, proxy_port
from openpyxl import Workbook
import socks
from models import User, AddUsers, Channel, Message

if proxy_host and proxy_port:
    client = TelegramClient('session_name', api_id, api_hash, proxy=(socks.SOCKS5, proxy_host, proxy_port))
else:
    client = TelegramClient('session_name', api_id, api_hash)
client.start()

Base = declarative_base()

session = DBSession()


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
                get_user_entity(new_message.inviter_id)
                new_message.action = action
            elif type(message.action) == MessageActionPinMessage:
                action = 'MessageActionPinMessage'
                new_message.action = action
            elif type(message.action) == MessageActionChatAddUser:
                action = 'MessageActionChatAddUser'
                new_message.action = action
                for user in message.action.users:
                    save_add_user(new_message.message_id, to_id, message.from_id, user, message.date, 'manually')
                    get_user_entity(user)
            elif type(message.action) == MessageActionChatDeleteUser:
                action = 'MessageActionChatDeleteUser'
                new_message.action = action

            elif type(message.action) == MessageActionChannelMigrateFrom:
                action = 'MessageActionChannelMigrateFrom'
                new_message.action = action
            else:
                print(message.action)
                print(message)
                raise (AssertionError("unknown action type" + type(message.action)))

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
            get_user_entity(new_message.from_id)
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


def get_user_entity(some_id):
    if not some_id:
        return None
    exist_user = None
    if type(some_id) == int:
        exist_user = session.query(User).filter_by(id=int(some_id)).first()
    if not exist_user:
        exist_user = session.query(User).filter_by(username=some_id).first()
    user_dict = dict()
    if exist_user:
        user_dict['id'] = exist_user.id
        user_dict['username'] = exist_user.username
    else:
        user = client.get_entity(some_id)
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
        user_dict['id'] = new_user.id
        user_dict['username'] = new_user.username
    return user_dict


def get_channel_entity(some_id):
    if not some_id:
        return None
    exist_channel = None
    if type(some_id) == int:
        exist_channel = session.query(Channel).filter_by(id=int(some_id)).first()
    if not exist_channel:
        exist_channel = session.query(Channel).filter_by(name=some_id).first()

    channel_dict = dict()
    if exist_channel:
        channel_dict['id'] = exist_channel.id
        channel_dict['name'] = exist_channel.name
    else:
        channel = client.get_entity(some_id)
        new_channel = Channel()
        new_channel.id = channel.id
        print(channel)
        new_channel.name = channel.title
        session.add(new_channel)
        session.commit()
        channel_dict['id'] = new_channel.id
        channel_dict['name'] = new_channel.name
    return channel_dict


def pull_channel_history(peer, min_id=0, max_id=0):
    if min_id and type(min_id) != 'int':
        print('start id must be int')
        return
    if min_id and  type(max_id) != 'int':
        print('end id must be int')
        return
    if not max_id:
        max_id = client.get_messages(peer).total
    for i in range(min_id, max_id // StepLength + 1):
        message_history = client.get_messages(peer, min_id=min_id + i, max_id=StepLength + i * StepLength)
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
