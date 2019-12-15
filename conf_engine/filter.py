# coding=utf-8
import sys
import logger
from abc import ABCMeta,abstractmethod

class Filter:
    __metaclass__ = ABCMeta

    def __init__(self):
        self.size = 0

    @abstractmethod
    def filte(self):
        pass
