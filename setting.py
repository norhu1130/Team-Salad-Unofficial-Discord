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

        # Twitter API
        self.twitter_api_key = "key"
        self.twitter_api_secret = "secret"
        self.twitter_access_token = "token"
        self.twitter_access_secret = "secret"