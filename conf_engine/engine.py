# coding=utf-8
import sys
import os
sys.path.append("%s/../" % os.path.dirname(os.path.abspath(__file__)))
import logger
import traceback
from mongoHelper import MongoHelper

class RuleEngine:
    def __init__(self):
        self.rules = []
        self.mongo_helper = MongoHelper("stock")

    def load(self, conf_pathfile):
        self.rules.append(rule)

    def run_once(self, force=False):
        for rule in self.rules:
            try:
                data = rule['collection']
            except Exception as e:
                logger.error("rule(%s) exception(%s)", str(rule), traceback.format_exc())

    def __readData(self, collection):
        hangseng_datas = self.mongo_helper.find(collection, {"date":self.date})
        logger.info_print("data: %s", hangseng_datas)
        if hangseng_datas:
            return hangseng_datas[0]
        else:
            return {}



if __name__ == "__main__":
    ruleEngine = RuleEngine()
    ruleEngine.load("")
    ruleEngine.run_once()
