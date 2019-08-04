# coding=utf-8
import sys
import logger
from abc import ABCMeta,abstractmethod
 
import * from engine_const
import Rule from rule_abstract

class SequenceMonotonicityRule(Rule):
    def __init__(self, sequences):
        Rule.__init__(self, sequences)
        self.m = 2 #连续单调变化次数

    def inspect(self):
        up_count = 0
        down_count = 0
        seqs = self.sequences
        for i in range(len(seqs)):
            warn=[]
            emerg=[]
            if i>0 and seqs[i-1] != '-' and seqs[i] != '-':
                if seqs[i] > seqs[i-1]:
                    up_count += 1
                    down_count=0
                elif seqs[i] < seqs[i-1]:
                    down_count += 1
                    up_count=0
                if up_count >= self.m:
                    warn.append("double up")
                if down_count >= self.m:
                    emerg.append("double down")
            self.append_warn(warn)
            self.append_emerg(emerg)
        return self.alerts


