# -*- coding:utf-8 -*-
from fet_tel_chat_record import pull_channel_history, export_add_user_list_to_excel_by_id

if __name__ == "__main__":
    pull_channel_history('GlobalParcelX')
    export_add_user_list_to_excel_by_id(1001353770)
