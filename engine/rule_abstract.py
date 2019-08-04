# coding=utf-8
import sys
import logger
from abc import ABCMeta,abstractmethod
from engine_const import * 

class Rule:
    #指定这是一个抽象类
    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    def append_emerg(self, emerg):
        self.alerts[EMERG].append(emerg)

    def append_warn(self, warn):
        self.alerts[WARN].append(warn)

    ###
    # output: {"emerg":["", ""], "warn":["",""]}
    @abstractmethod
    def inspect(self):
        pass

    @abstractmethod
    def name(self):
        pass


