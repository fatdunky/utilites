'''
Created on 23Nov.,2016

@author: fatdunky
'''
import ConfigParser, os, logging

class ConfigurationParser(object):
    '''
    This class reads the configuration file and returns a coinfiguration object
    '''

   
    def __init__(self, default_config_dir, default_config_file):
        '''
        Constructor
        ''' 
        self.__config = ConfigParser.ConfigParser()
        self.__default_config_dir = default_config_dir
        self.__default_config_file = default_config_file
        self.__config_directory = os.getcwd() + os.path.sep + self.__default_config_dir
        self.__config_file = self.__config_directory + os.path.sep + self.__default_config_file


    def set_config_directory(self, directory):
        if os.path.isdir(directory):
            self.__config_directory = directory
            logging.debug("Setting configuration directory to: %s",directory)
        else:
            default_directory = os.getcwd() + os.path.sep + self.__default_config_dir
            self.__config_directory = default_directory
            logging.info("Specified configuration directory %s, did not exist. Using default directory: %s",directory,default_directory)
         
    def read_config(self, configuration_file_name): 
        '''
        Check if configuration directory exits
        '''
        included_path = os.path.dirname(configuration_file_name)
        configuration_file_name = os.path.basename(configuration_file_name)
        if included_path != "":
            self.set_config_directory(included_path)
        
        if self.__config_directory is None or self.__config_directory == "":
            default_directory = os.getcwd() + os.path.sep + self.__default_config_dir
            self.set_config_directory(default_directory)
            logging.info("Configuration Directory no set, using default directory: %s",default_directory)

        if os.path.isfile(configuration_file_name): 
            self.__config.read(configuration_file_name)
            logging.debug("Setting configuration file to: %s",configuration_file_name)
        else:
            default_file = self.__config_directory + os.path.sep + self.__default_config_file
            self.__config.read(default_file)
            logging.info("Specified configuration file %s, did not exist. Using default file: %s",configuration_file_name,default_file)  
            
    def get_config(self):
        return self.__config


    def get_config_file(self):
        return self.__config_file
    
    def get_config_directory(self):
        return self.__config_directory

    def set_config_file(self, value):
        if os.path.isdir(value):
            self.__config_file = value
            logging.debug("Setting configuration file to: %s",value)
        else:
            default_file = self.get_config_directory() + os.path.sep + self.__default_config_file
            self.__config_file = default_file
            logging.info("Specified configuration file %s, did not exist. Using default file: %s",value,default_file)
         
    def del_config_file(self):
        del self.__config_file
    
    def del_config_directory(self):
        del self.__config_directory
    
    def get_default_config_dir(self):
        return self.__default_config_dir


    def get_default_config_file(self):
        return self.__default_config_file


    def set_default_config_dir(self, value):
        self.__default_config_dir = value


    def set_default_config_file(self, value):
        self.__default_config_file = value


    def del_default_config_dir(self):
        del self.__default_config_dir


    def del_default_config_file(self):
        del self.__default_config_file

    config = property(fget=get_config, fset=None, fdel=None, doc="configuration object produced by python's configuration parser")
    config_file = property(get_config_file, set_config_file, del_config_file, "Configuration file to read")
    config_directory = property(get_config_directory, set_config_directory, del_config_directory, "The configuration file's directory")
    default_config = property(get_default_config_dir, set_default_config_dir, del_default_config_dir, "default_config's docstring")
    default_config_file = property(get_default_config_file, set_default_config_file, del_default_config_file, "default_config_file's docstring")
