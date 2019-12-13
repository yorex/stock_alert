# coding=utf-8
import sys
import logger
from abc import ABCMeta,abstractmethod

class Rule:
    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    @abstractmethod
    def transform(self):
        pass

    @abstractmethod
    def name(self):
        pass

