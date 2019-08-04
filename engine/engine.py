# coding=utf-8
import sys
import os
sys.path.append("%s/../" % os.path.dirname(os.path.abspath(__file__)))
import logger
from engine_const import *
import traceback
from rule_spec_hangseng import *

class RuleEngine:
    def __init__(self):
        self.rules = []

    def add_rule(self, rule):
        self.rules.append(rule)

    def inspect(self, force=False):
        for rule in self.rules:
            try:
                alert = rule.inspect(force)
            except Exception as e:
                logger.error("rule(%s) exception(%s)", str(rule), traceback.format_exc())


if __name__ == "__main__":
    ruleEngine = RuleEngine()
    ruleEngine.add_rule(SpecHangsengRule())
    ruleEngine.inspect()
