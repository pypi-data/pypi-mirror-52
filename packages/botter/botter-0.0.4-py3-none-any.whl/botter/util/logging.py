from abc import ABC
from logging import Logger, getLogger

class Logging(ABC):
    __logger: Logger = None
    logger_name: str
    
    def __init__(self):
        self.init_logger()
    
    @property
    def logger(self) -> Logger:
        if (self.__logger is None):
            self.init_logger()
        return self.__logger
    
    def init_logger(self):
        if (getattr(self, 'logger_name', None) is None):
            self.logger_name = self.__module__.replace('_', '-')
        
        self.__logger = getLogger(self.logger_name)

__all__ = \
[
    'Logging',
]
