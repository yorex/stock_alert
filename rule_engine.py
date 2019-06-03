import sys
import MaHelper
from abc import ABCMeta,abstractmethod
 
EMERG="emerg"
WARN="warn"

DT_BALANCES="balances"

class Rule:
    __metaclass__ = ABCMeta #指定这是一个抽象类

    def __init__(self):
        self.alerts = {EMERG:[], WARN:[]}

    def append_emerg(self, emerg):
        if not emerg and len(emerg) > 0:
            self.alerts[EMERG].append(emerg)

    def append_warn(self, warn):
        if not warn and len(warn) > 0:
            self.alerts[WARN].append(warn)

    ###
    # output: {"emerg":["", ""], "warn":["",""]}
    @abstractmethod
    def inspect(self):
        pass

class BalanceMA5Rule(Rule):
    def __init__(self, balances):
        self.balances = balances
        self.helper = MaHelper()

    def inspect(self):
        n = 5
        m = 3 #连续单调变化次数
        ma5 = self.helper(n, balances)
        up_count = 0
        down_count = 0
        for i in range(len(balances)):
            warn=[]
            emerg=[]
            if i>0 and balances[i-1] != '-' and balances[i] != '-':
                if balances[i] > balances[i-1]:
                    up_count++
                    down_count=0
                elif balances[i] < balances[i-1]:
                    down_count++
                    up_count=0
                if up_count > m:
                    warn.append("连续3递增")
                if down_count > m:
                    emerg.append("连续3递减")
            append_warn(warn)
            append_emerg(emerg)
        return self.alerts

class RuleEngine:
    def __init__(self, **kwargs):
        self.ctx = kwargs
        self.rules = []
        if kwargs.has_key(DT_BALANCES)):
            self._add_rule(Balance(kwargs[DT_BALANCES]))

    def _add_rule(self, rule):
        self.rules.append(rule)

    def inspect(self):
        alerts = {EMERG:[], WARN:[]}
        for rule in self.rules:
            try:
                alert = rule.inspect()
                if alerts.has_key(EMERG):
                    alerts[EMERG] += alert[EMERG]
                if alerts.has_key(WARN):
                    alerts[WARN] += alert[WARN]
            except Exception as e:
                print "rule(%s) exception(%s)" % (str(rule), e)
        return alerts


        
