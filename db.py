#-*- coding:utf-8 -*-
import MySQLdb
import MySQLdb.cursors
import MySQLdb.converters
import traceback
from log import logger
from DBUtils.PooledDB import PooledDB
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
        self.dbpool = self.db_init()

    @mysql_retry_func("failed to connect to host %s, db %s" % (db_settings.host, db_settings.database))
    def db_init(self):
        conv=MySQLdb.converters.conversions.copy()
        conv[246]=float
        dbpool = PooledDB(creator=MySQLdb,maxusage=1000,host=db_settings.host,user=db_settings.user,\
                          passwd=db_settings.passwd,port=db_settings.port,\
                          db=db_settings.database,cursorclass=MySQLdb.cursors.DictCursor, conv=conv)
        
        return dbpool
            
    @mysql_retry_func("failed to execute sql to host %s, db %s" % (db_settings.host, db_settings.database))
    def db_execute(self, sql, hargs=()):
        try:
            conn = self.dbpool.connection()
            cur = conn.cursor()
            cur.execute("set names utf8")
            cur.execute(sql, hargs)
            conn.commit()
            dataset = cur.fetchall()
            cur.close()
            conn.close()
            return dataset
        except:
            logger.log_error("sql excute error:\n\tsql:%s\n\thargs:%s" % (sql, hargs))
            raise

db = DB()
        
if __name__ == "__main__":
    l = db.db_execute("desc t_field %s")
    for i in l:
        print i
