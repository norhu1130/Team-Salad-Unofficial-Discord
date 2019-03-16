# -*- coding:utf-8 -*- 

import os, datetime, setting

Setting = setting.Settings()

def log_msg(server, server_id, channel, channel_id, usr, usr_tag, usr_id, msg):
    now = datetime.datetime.now()
    try:
        if os.path.isfile("log/%s" % (Setting.log_file)):
            if os.path.isfile("Server_%s/prefix.setting" % (server_id)):
                f = open("log/%s" % (Setting.log_file), 'r', encoding="UTF8")
                old_log_info = f.read()
                f.close()
                log_info = old_log_info + "\n%s / %s / %s | %s : %s | Server : %s(%s) | Channel : %s(%s) | Author : %s%s(%s) | Message : %s" % (now.year, now.month, now.day, now.hour, now.minute, server, server_id, channel, channel_id, usr, usr_tag, usr_id, msg)
                f = open("log/%s" % (Setting.log_file), 'w', encoding="UTF8")
                f.write(log_info)
                f.close()
            else:
                print("메시지 로깅 모듈(msg_log.py)로부터 메시지 로깅을 거부당했습니다.\n사유 : 해당 서버(%s(%s))에 봇이 활성화 되지 않았습니다!\n\n==============\n" % (server, server_id))
        else:
            if os.path.isfile("Server_%s/prefix.setting" % (server_id)):
                log_info = "%s / %s / %s | %s : %s | Server : %s(%s) | Channel : %s(%s) | Author : %s%s(%s) | Message : %s" % (now.year, now.month, now.day, now.hour, now.minute, server, server_id, channel, channel_id, usr, usr_tag, usr_id, msg)
                f = open("log/%s" % (Setting.log_file), 'w', encoding="UTF8")
                f.write(log_info)
                f.close()
                print("%s 파일을 발견하지 못하여 해당 파일을 생성하였습니다.\n\n==============\n" % ("log/%s" % (Setting.log_file)))
            else:
                print("메시지 로깅 모듈(msg_log.py)로부터 메시지 로깅을 거부당했습니다.\n사유 : 해당 서버(%s(%s))에 봇이 활성화 되지 않았습니다!\n\n==============\n" % (server, server_id))
    except Exception as e:
        print("msg log error : %s" % (e))
        pass

def log_start_msg():
    now = datetime.datetime.now()
    if os.path.isfile("log/%s" % (Setting.log_file)):
        f = open("log/%s" % (Setting.log_file), 'r', encoding="UTF8")
        old_log_info = f.read()
        f.close()
        log_info = old_log_info + "\n\n%s / %s / %s | %s : %s | Logging Started.\n" % (now.year, now.month, now.day, now.hour, now.minute)
        f = open("log/%s" % (Setting.log_file), 'w', encoding="UTF8")
        f.write(log_info)
        f.close()
    else:
        log_info = "%s / %s / %s | %s : %s | Logging Started.\n" % (now.year, now.month, now.day, now.hour, now.minute)
        f = open("log/%s" % (Setting.log_file), 'w', encoding="UTF8")
        f.write(log_info)
        f.close()
        print("%s 파일을 발견하지 못하여 해당 파일을 생성하였습니다.\n\n==============\n" % ("log/%s" % (Setting.log_file)))