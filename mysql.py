# -*- coding:utf-8 -*- 

import pymysql, setting

Setting = setting.Settings()

def mysql_remove_table_content(tablename):
    try:
        connect = pymysql.connect(host=Setting.mysql_ip, user=Setting.mysql_id, password=Setting.mysql_pw, db=Setting.mysql_db, charset='utf8mb4')
        try:
            with connect.cursor() as cur:
                query = 'DELETE FROM %s' % (tablename)
                cur.execute(query)
            connect.commit()
        finally:
            connect.close()
    except Exception as e:
        print("Mysql Error : %s" % (e))

def mysql_add_table_content(tablename, rowname, queue):
    try:
        connect = pymysql.connect(host=Setting.mysql_ip, user=Setting.mysql_id, password=Setting.mysql_pw, db=Setting.mysql_db, charset='utf8mb4')
        try:
            with connect.cursor() as cur:
                query = 'UPDATE `%s` SET `%s`=%s' % (tablename, rowname, queue)
                cur.execute(query)
            connect.commit()
        finally:
            connect.close()
    except Exception as e:
        print("Mysql Error : %s" % (e))