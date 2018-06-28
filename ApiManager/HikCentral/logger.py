# encoding: utf-8
import time, os


# log记录类
class LogRecord:
    def __init__(self):
        self.logfile = os.getcwd() + '\\TestReport\\log.txt'
        self.initLogFile()

    def __del__(self):
        pass

    def initLogFile(self):
        dateTime = time.strftime("%Y-%m-%d %H:%M:%S")
        with open(self.logfile, 'w') as logFile:
            logFile.write('=============== [' + str(dateTime) + ', Begin to record...] ===============\r')

    def writeText2Log(self, strContent, log_type=0):
        log_prefix = ''
        if log_type == 0:
            log_prefix = 'Info'
        elif log_type == 1:
            log_prefix = 'Warning'
        else:
            log_prefix = 'Error'

        with open(self.logfile, 'a+', 1) as logFile:
            logFile.write('[%s]: %s\r%s\r' % (log_prefix, time.strftime("%Y-%m-%d %H:%M:%S"), strContent))

    def write2log(self, content, log_prefix):
        with open(self.logfile, 'a+', 1) as logFile:
            logFile.write('[%s]: %s\r%s\r' % (log_prefix, time.strftime("%Y-%m-%d %H:%M:%S"), content))

    def log_info(self, content):
        self.write2log(content, 'Info')

    def log_warning(self, content):
        self.write2log(content, 'Warning')

    def log_error(self, content):
        self.write2log(content, 'Error')