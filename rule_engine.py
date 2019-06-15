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

    def __init__(self, app):
        self.alerts = {EMERG:[], WARN:[]}
        self.app = app

    def append_emerg(self, emerg):
        self.alerts[EMERG].append(emerg)

    def append_warn(self, warn):
        self.alerts[WARN].append(warn)

    ###
    # output: {"emerg":["", ""], "warn":["",""]}
    @abstractmethod
    def inspect(self):
        pass

class SequenceMonotonicityRule(Rule):
    def __init__(self, app, sequences):
        Rule.__init__(self, app)
        self.sequences = sequences
        logger.info(self.app, "SequenceMonotonicityRule.sequences: %s", str(sequences))

    def inspect(self):
        m = 2 #连续单调变化次数
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
                if up_count >= m:
                    warn.append("double up")
                if down_count >= m:
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
                logger.info(self.app, "rule(%s) output(%s)", str(rule), alert)
                if alert[EMERG]:
                    alerts[EMERG] += alert[EMERG]
                if alert[WARN]:
                    alerts[WARN] += alert[WARN]
            except Exception as e:
                logger.error(self.app, "rule(%s) exception(%s)", str(rule), e)
        return alerts


        
