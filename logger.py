'''
Created on 3Dec.,2016

@author: fatdunky
'''
import logging, os, time

from logging.handlers import TimedRotatingFileHandler, RotatingFileHandler
from MyTimedRotatingFileHandler import MyTimedRotatingFileHandler

class Logger(object):
    '''
    This class handles the logging for the application
    '''
    DEFAULT_LOGGER_FORMAT='%(asctime)s|%(name)s|%(levelname)s|%(message)s'
    DEFAULT_LOGGER_DATE_FORMAT='%Y%m%d|%H:%M:%S'
    DEFAULT_CONFIG_DIR='config'
    DEFAULT_CONFIG_FILE='config.cfg'
    DEFAULT_DATA_DIR='data'
    DEFAULT_LOG_DIR='logs'
    DEFAULT_LOG_FILE_START='output'
    DEFAULT_LOG_FILE_SUFFIX='.log'
    DEFAULT_LOG_LEVEL=logging.DEBUG
    
    DEFAULT_LOG_ROTATE_MODE='size'
    DEFAULT_LOG_ROTATE_WHEN='midnight'
    DEFAULT_LOG_ROTATE_INTERVAL=1
    DEFAULT_LOG_ROTATE_BACKUP_COUNT=30
    DEFAULT_LOG_ROTATE_BYTES=1000000
        
    _console_logging = False
    _rotate_log_mode = DEFAULT_LOG_ROTATE_MODE
    _log_directory = os.getcwd() + os.path.sep + DEFAULT_LOG_DIR
    _log_file = DEFAULT_LOG_FILE_START + DEFAULT_LOG_FILE_SUFFIX
    _format_string = DEFAULT_LOGGER_FORMAT
    _format_date_string = DEFAULT_LOGGER_DATE_FORMAT
    _log_level = DEFAULT_LOG_LEVEL
    _log_file_date = time.strftime("%Y%m%d")
           
    _rotate_log_mode = DEFAULT_LOG_ROTATE_MODE
    _when = DEFAULT_LOG_ROTATE_WHEN
    _interval = DEFAULT_LOG_ROTATE_INTERVAL
    _backup_count = DEFAULT_LOG_ROTATE_BACKUP_COUNT
    _bytes = DEFAULT_LOG_ROTATE_BYTES
        
    _levelNames = {
    logging.CRITICAL : 'CRITICAL',
    logging.ERROR : 'ERROR',
    logging.WARNING : 'WARNING',
    logging.INFO : 'INFO',
    logging.DEBUG : 'DEBUG',
    logging.NOTSET : 'NOTSET',
    'CRITICAL' : logging.CRITICAL,
    'ERROR' : logging.ERROR,
    'WARN' : logging.WARNING,
    'WARNING' : logging.WARNING,
    'INFO' : logging.INFO,
    'DEBUG' : logging.DEBUG,
    'NOTSET' : logging.NOTSET,
    }
    
    def __init__(self):
        '''
        Constructor
        '''
    @staticmethod
    def create_timed_csv_logger(file_name, when, interval, backup_count, logger_name, header):
        # create logger
        log = logging.getLogger(logger_name)
        
        # create time-rotating log handler
        logHandler = MyTimedRotatingFileHandler(file_name, when, interval, backup_count, header, log)
        form = '%(message)s'
        logFormatter = logging.Formatter(form)
        logHandler.setFormatter(logFormatter)
        
        #Configure logger
        log.addHandler(logHandler)
        log.setLevel(logging.INFO)
        log.info("%s", header)
        
        return log
    
    
    
    @staticmethod
    def set_console_logging(boolean_value):
        '''
        set console logging value
        '''
        if type(boolean_value) == bool:
            Logger._console_logging = boolean_value
            logging.debug("Setting console_logging to %s", boolean_value)    
        else:
            Logger._console_logging = False
            logging.error("Non boolean value passed setting console to False")     
        
    @staticmethod
    def get_console_logging():
        return Logger._console_logging       
    
    @staticmethod
    def set_log_directory(log_directory):
        '''
        set logging Directory
        '''
        if log_directory and os.path.isdir(log_directory):
            Logger._log_directory = log_directory
            logging.debug("Setting logging directory to: %s",log_directory)
        else:
            _default_directory = os.getcwd() + os.path.sep + Logger.DEFAULT_LOG_DIR
            Logger._log_directory = _default_directory
            logging.error("Specified logging directory %s, did not exist. Using default directory: %s",log_directory,_default_directory)
    
    @staticmethod           
    def get_log_directory():
        return Logger._log_directory
    
    @staticmethod              
    def set_log_file(log_file):
        '''
        set logging file
        '''
        included_path=""
        
        if log_file and log_file != "":
            included_path = os.path.dirname(log_file)
            log_file = os.path.basename(log_file)
            
        if included_path != "":
            Logger.set_log_directory(included_path)
            
        if log_file is None or log_file == "":
            #defaultLogFile = Constants.DEFAULT_LOG_FILE_START +  self.logFileDate +  Constants.DEFAULT_LOG_FILE_SUFFIX
            _default_log_file = Logger.DEFAULT_LOG_FILE_START +  Logger.DEFAULT_LOG_FILE_SUFFIX
            Logger._log_file = _default_log_file
            logging.error("Specified logging file was null. Using default file: %s",_default_log_file)
        else:        
            Logger._log_file = log_file
            logging.debug("Setting logging logFile to: %s",log_file)
    
    @staticmethod             
    def get_log_file():
        return Logger._log_file 
    
    @staticmethod
    def get_full_path_log_file():
        return Logger.get_log_directory() + os.path.sep + Logger.get_log_file()
        
    @staticmethod
    def set_format_string(string_value):
        '''
        set logging format string
        '''
        if string_value is None or string_value == "":
            Logger._format_string = Logger.DEFAULT_LOGGER_FORMAT
            logging.error("Empty value passed to set_format_string, using default value")     
        
        Logger._format_string=string_value
               
    @staticmethod
    def get_format_string():
        return Logger._format_string
    
    @staticmethod
    def set_date_format_string(string_value):
        '''
        set logging format date string
        '''
        if string_value is None or string_value == "":
            Logger._format_date_string = Logger.DEFAULT_LOGGER_DATE_FORMAT
            logging.error("Empty value passed to setDateFormatString, using default value")     
        
        Logger._formatDateString=string_value
               
    @staticmethod
    def get_date_format_string():
        return Logger._format_date_string
    
    @staticmethod
    def set_logging_level(level):
        '''
        sets the logging level
        '''
        if str(level) == level:
            if level not in Logger._levelNames:
                logging.error("Unknown logging level specified: %s, setting to %s",level,Logger._levelNames[Logger.DEFAULT_LOG_LEVEL])
                logging.getLogger().setLevel(Logger.DEFAULT_LOG_LEVEL)
                Logger._log_Level = Logger.DEFAULT_LOG_LEVEL

            level = Logger._levelNames[level]
        

        if isinstance(level, (int, long)):
            logging.getLogger().setLevel(level)
            Logger._log_level = level
            logging.info("Setting log level to %s",Logger._levelNames[level])
        else:
            logging.error("Unknown logging level specified: %s, setting to %s",level,Logger._levelNames[Logger.DEFAULT_LOG_LEVEL])
            logging.getLogger().setLevel(Logger.DEFAULT_LOG_LEVEL)
            Logger._log_Level = Logger.DEFAULT_LOG_LEVEL
    
    @staticmethod
    def get_logging_level():
        return Logger._log_level
    
    @staticmethod
    def set_rotation_file(mode=DEFAULT_LOG_ROTATE_MODE, when=DEFAULT_LOG_ROTATE_WHEN, interval=DEFAULT_LOG_ROTATE_INTERVAL, backup_count=DEFAULT_LOG_ROTATE_BACKUP_COUNT, bytes=DEFAULT_LOG_ROTATE_BYTES):
       
        Logger._rotate_log_mode = mode
        Logger._when = when
        Logger._interval = interval
        Logger._backup_count = backup_count
        Logger._bytes = bytes
        
    @staticmethod        
    def update_handler():
        '''
        configure the logger
        '''

        if Logger._log_directory is None or Logger._log_directory == "":
            Logger.set_log_directory("")
            
        if Logger._log_file is None or Logger._log_file == "":
            Logger.set_log_file("")
        
        
        else:
            if Logger._rotate_log_mode.upper() == "TIME" or Logger._rotate_log_mode.upper() == "TIMED" :        
                Logger._handler = TimedRotatingFileHandler(Logger.get_full_path_log_file(), when=Logger._when, interval=Logger._interval, backupCount=Logger._backup_count, encoding=None, delay=False, utc=False)
            elif  Logger._rotate_log_mode.upper() == "SIZE":
                Logger._handler = RotatingFileHandler(Logger.get_full_path_log_file(),maxBytes=Logger._bytes,backupCount=Logger._backup_count, encoding=None, delay=False)
            else:
                Logger._handler = logging.FileHandler(Logger.get_full_path_log_file(), encoding=None, delay=False)
                
        if Logger._format_string is None or Logger._format_string == "":
            Logger.set_format_string("")
        
        if Logger._log_level is None or Logger._log_level == "":
            Logger.set_logging_level("")
        
        formatter = logging.Formatter(fmt=Logger.get_format_string(), datefmt=Logger.get_date_format_string())
        Logger._handler.setFormatter(formatter)
        Logger._handler.setLevel(Logger.get_logging_level())
        logging.getLogger().addHandler(Logger._handler)


        
        #logging.basicConfig(filename=self.getFullPathLogFile(),format=self.formatString,level=self.logLevel)     
    
    @staticmethod
    def rotate_log():
        '''
        TODO: Setup logrotation 
        '''
        logging.info("LogRotation")