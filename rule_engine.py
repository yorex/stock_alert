# coding=utf-8
import sys
import logger
from abc import ABCMeta,abstractmethod
 
EMERG="emerg"
WARN="warn"

DT_BALANCES="balances"

class Rule:
    #指定这是一个抽象类
    __metaclass__ = ABCMeta

    def __init__(self, app, sequences):
        self.alerts = {EMERG:[], WARN:[]}
        self.app = app
        self.sequences = sequences
        logger.debug("SequenceMonotonicityRule.sequences: %s", str(sequences))

    def append_emerg(self, emerg):
        self.alerts[EMERG].append(emerg)

    def append_warn(self, warn):
        self.alerts[WARN].append(warn)

    ###
    # output: {"emerg":["", ""], "warn":["",""]}
    @abstractmethod
    def inspect(self):
        pass

class RapidDownRule(Rule):
    def __init__(self, app, sequences, threshold):
        Rule.__init__(self, app, sequences)
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

class SequenceMonotonicityRule(Rule):
    def __init__(self, app, sequences):
        Rule.__init__(self, app, sequences)
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


class RuleEngine:
    def __init__(self, app):
        self.rules = []
        self.app = app

    def add_rule(self, rule):
        self.rules.append(rule)

    def inspect(self):
        alerts = {EMERG:[], WARN:[]}
        for rule in self.rules:
            try:
                alert = rule.inspect()
                logger.info("rule(%s) output(%s)", str(rule), alert)
                if alert[EMERG]:
                    alerts[EMERG] += alert[EMERG]
                if alert[WARN]:
                    alerts[WARN] += alert[WARN]
            except Exception as e:
                logger.error("rule(%s) exception(%s)", str(rule), e)
        return alerts


        
