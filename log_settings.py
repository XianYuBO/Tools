#-*- coding:utf-8 -*-

LOG_LEVEL = 'debug'




if LOG_LEVEL.upper() not in ['DEBUG', 'INFO', 'WARNING', 'ERROR']:
    raise Exception("No such log level",  LOG_LEVEL)
    exit(-1)
