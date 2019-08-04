# coding=utf-8
import sys
import os
sys.path.append("%s/../" % os.path.dirname(os.path.abspath(__file__)))
print(sys.path)

from engine_const import *
from rule_abstract import *
import logger
import mongoHelper

class SpecHangsengRule(Rule):
    def __init__(self):
        Rule.__init__(self)
        self.mongo_helper = mongoHelper.MongoHelper('127.0.0.1', 'stock', 'hangseng_index')

    def name(self):
        return "spec_hangseng"
    
    def get_percent(self, before, now):
        return 1.0*(now - before) / before
    
    # force=true 表示强制计算全部告警
    def inspect(self, force=False):
        datas = self.mongo_helper.find({})
        begin = 0
        if not force:
            # 定位到最近的未告警的记录
            for data in datas:
                if data.has_key(ALERT_EMERGS) and data[ALERT_EMERGS].has_key(self.name()) or data.has_key(ALERT_WARNS) and data[ALERT_WARNS].has_key(self.name()):
                    begin+=1
                    continue
        logger.info("SpecHangsengRule set range begin at index(%d)" % begin)

        for i in range(begin, len(datas)):
            emerg=[]
            warn=[]
            # if rapid down, check situation
            if i>=1 and self.get_percent(datas[i-1]["dclose"], datas[i]["dclose"]) < -0.25:
                emerg.append("极降，确认原因; 是否极端事件?")
            if i>=3 and datas[i-3]["dclose"] > datas[i-2]["dclose"] > datas[i-1]["dclose"] > datas[i]["dclose"]:
                # if continue 3 down, 50% cut
                emerg.append("连续3降，cut 50%")
            elif i>=2 and datas[i-2]["dclose"] > datas[i-1]["dclose"] > datas[i]["dclose"]:
                # if continue 2 down, 20% cut
                warn.append("连续2降，cut 20%")
            datas[i].setdefault(ALERT_EMERGS, {})[self.name()]=emerg
            datas[i].setdefault(ALERT_WARNS, {})[self.name()]=warn

            self.mongo_helper.update({"_id":datas[i]["_id"]}, datas[i])


if __name__ == "__main__":
    rule = SpecHangsengRule()
    rule.inspect(True)
