# -*- coding: utf-8 -*- 

import datetime, sys

class Settings:
    def __init__(self):
        self.token = "token"
        self.prefix = "="
        self.version = "version"
        self.log_file = "msg.log"
        self.bot_admin = "id"
        self.online_notice_channel = "id"
        self.error_notice_channel = "id"
        self.copy = "© %s Your Team." % datetime.datetime.now().year

        # "0x" + Hex CODE 6 digits
        self.error_embed_color = 0xff0000
        self.embed_color = 0x7bf7d0

        # Mysql
        self.mysql_ip = "ip"
        self.mysql_id = "id"
        self.mysql_pw = "pw"
        self.mysql_db = "db"

        # Naver API
        self.naver_api_id = "id"
        self.naver_api_secret = "secret"

# ------ 이 아래는 건들지 마세요 ----- #

import ctypes

class MEMORYSTATUSEX(ctypes.Structure):
    _fields_ = [
        ("dwLength", ctypes.c_ulong),
        ("dwMemoryLoad", ctypes.c_ulong),
        ("ullTotalPhys", ctypes.c_ulonglong),
        ("ullAvailPhys", ctypes.c_ulonglong),
        ("ullTotalPageFile", ctypes.c_ulonglong),
        ("ullAvailPageFile", ctypes.c_ulonglong),
        ("ullTotalVirtual", ctypes.c_ulonglong),
        ("ullAvailVirtual", ctypes.c_ulonglong),
        ("sullAvailExtendedVirtual", ctypes.c_ulonglong),
    ]

    def __init__(self):
        self.dwLength = ctypes.sizeof(self)
        super(MEMORYSTATUSEX, self).__init__()