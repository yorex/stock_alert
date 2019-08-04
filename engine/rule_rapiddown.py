# coding=utf-8
import sys
import logger
import * from engine_const
import Rule from rule_abstract

class RapidDownRule(Rule):
    def __init__(self, sequences, threshold):
        Rule.__init__(self, sequences)
        self.down_threshold = threshold
    
    def inspect(self):
        seqs = self.sequences
        for i in range(len(seqs)):
            emerg=[]
            warn=[]
            if i > 0 and (seqs[i-1] - seqs[i])/seqs[i-1] > self.down_threshold:
                emerg.append("急跌,往往是形势转折点,退出观察为妙")
            self.append_warn(warn)
            self.append_emerg(emerg)
        return self.alerts


