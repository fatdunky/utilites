'''
Created on 11 Dec. 2017

@author: mcrick
'''
from logging.handlers import TimedRotatingFileHandler


class MyTimedRotatingFileHandler(TimedRotatingFileHandler):
    '''
    classdocs
    '''

    def __init__(self, logfile, when, interval, backupCount, header = "", header_log = None):
        TimedRotatingFileHandler.__init__(self,logfile, when, interval, backupCount)
        #super(MyTimedRotatingFileHandler, self).__init__(logfile, when, interval, backupCount)
        self.configureHeaderWriter(header,header_log)

    def doRollover(self):
        TimedRotatingFileHandler.doRollover(self)
        #super(MyTimedRotatingFileHandler, self).doRollover()
        if self._log is not None and self._header != "":
            self._log.info(self._header)

    def setHeader(self, header):
        self._header = header

    def configureHeaderWriter(self, header, log):
        self._header = header
        self._log = log
