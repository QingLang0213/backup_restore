# -*- coding: UTF-8 -*-

import sys
from ConfigParser import ConfigParser

class GetConfigs(object):
    """Get a option value from a given section."""
    
    def __init__(self):
        self.config = ConfigParser()
        self.path=sys.path[0] + "\\common\\"
        
        
    def getint(self, section, option, filename, exc=0):
        """return an integer value for the named option.
        return exc if no the option. 
        """
        try:
            self.config.read(self.path+filename+".ini")
            return self.config.getint(section, option)
        except Exception,e:
            print e
            return exc
        
    def getstr(self, section, option, filename, exc=None):
        """return an string value for the named option."""
        try:
            self.config.read(self.path+filename+".ini")
            return self.config.get(section,option)
        except Exception,e:
            print e
            return exc
        
    def get_list(self, section, option, filename, exc=[]):
        """return an list value for the named option."""
        try:
            self.config.read(self.path+filename +".ini")
            
            return self.config.get(section,option).split(',')
        except Exception,e:
            print e
            return exc      

            
