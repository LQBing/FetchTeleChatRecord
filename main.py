# -*- coding:utf-8 -*-
from lib import pull_channel_history, export_add_user_list_to_excel_by_id, get_channel_entity, get_user_entity
import sys


def help_info(arg_name=None):
    argv_list = ['gc', 'gu', 'pc']
    if (arg_name not in argv_list) or (arg_name == 'gc'):
        print('-- gc  ---- get channel id and name')
        print('gc <channel id | channel name>')
    if (arg_name not in argv_list) or (arg_name == 'gu'):
        print('-- gu  ----  get user id and username')
        print('gu <user id | user id>')
    if (arg_name not in argv_list) or (arg_name == 'pc'):
        print('-- pc  ----  pull channel history')
        print('pc <channel id | channel name> <start message id>')


if __name__ == "__main__":
    arg_list = sys.argv
    if len(arg_list) == 1:
        help_info()
    else:
        if arg_list[1] == 'gc':
            if len(arg_list) == 2:
                help_info(arg_list[1])
            else:
                print(get_channel_entity(arg_list[2]))
        elif arg_list[1] == 'gu':
            if len(arg_list) == 2:
                help_info(arg_list[1])
            else:
                print(get_user_entity(arg_list[2]))
        elif arg_list[1] == 'pc':
            if len(arg_list) == 2:
                help_info(arg_list[1])
            elif len(arg_list) == 3:
                pull_channel_history(arg_list[2])
            elif len(arg_list) == 4:
                pull_channel_history(arg_list[2], arg_list[3])
            else:
                pull_channel_history(arg_list[2], arg_list[3], arg_list[4])
