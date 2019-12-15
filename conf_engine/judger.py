# coding=utf-8
import sys
import logger
from abc import ABCMeta,abstractmethod

class Judger:
    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    @abstractmethod
    def judge(self):
        pass

