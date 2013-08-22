#-*- coding:utf-8 -*-
import MySQLdb
import MySQLdb.cursors
import MySQLdb.converters
import traceback
from log import logger

import db_settings

#强制性的要求输入出错信息
def mysql_retry_func(msg):
    def _mysql_retry_func(func):
        def __mysql_retry_func(*args, **kwargs):
            count = 0
            while True:
                count +=1
                if count > db_settings.restart_times:
                    raise Exception(msg)
                    exit(-1)
                try:
                    return func(*args, **kwargs)
                except MySQLdb.Error, e:
                    logger.log_error("mysql error %d: %s" % (e.args[0], e.args[1]))
                    continue
                except:
                    logger.log_error(traceback.format_exc())
                    continue            
        return __mysql_retry_func
    return _mysql_retry_func


class DB:
    def __init__(self):
        self.conn, self.cur = self.db_init()

    @mysql_retry_func("failed to connect to host %s, db %s" % (db_settings.host, db_settings.database))
    def db_init(self):
        conv=MySQLdb.converters.conversions.copy()
        conv[246]=float
        conn = MySQLdb.connect(host=db_settings.host,user=db_settings.user,\
                               passwd=db_settings.passwd,port=db_settings.port, \
                               cursorclass=MySQLdb.cursors.DictCursor, conv=conv)
        conn.select_db(db_settings.database)
        cur = conn.cursor()
        sql = "set names utf8"
        self.db_execute(sql)
        return conn, cur
            
    @mysql_retry_func("failed to execute sql to host %s, db %s" % (db_settings.host, db_settings.database))
    def db_execute(self, sql, hargs=()):
        try:
            self.cur.execute(sql, hargs)
            self.conn.commit()
            return self.cur
        except:
            logger.log_error("sql excute error:\nsql:%s\nhargs:%s" % (sql, hargs))
            raise

db = DB()
        
if __name__ == "__main__":
    l = db.db_execute("descd t_field %s")
    for i in l:
        print i
