from dingtalk_sender import DingTalkSender
from mongoHelper import MongoHelper
import time
import json

ALERT_WARNS="alert_warns"
ALERT_EMERGS="alert_emergs"


class AlertSummary:
    def __init__(self):
        self.mongo_helper = MongoHelper("127.0.0.1", "stock")
        self.today = time.strftime("%Y%m%d", time.localtime())
        self.collections = ["hangseng_index"]

    def generateSummary(self):
        content = [self.today]
        for collection in self.collections:
            collcont =  {}
            hangseng_data = self.readDataToday(collection)
            if hangseng_data.has_key(ALERT_EMERGS):
                collcont[collection+"-"+ALERT_EMERGS] = hangseng_data[ALERT_EMERGS]
            if hangseng_data.has_key(ALERT_WARNS):
                collcont[collection+"-"+ALERT_WARNS] = hangseng_data[ALERT_WARNS]
            content.append(collcont)
        return content


    def getScoreToday(self):
        score = 0
        for collection in self.collections:
            hangseng_data = self.readDataToday(collection)
            if hangseng_data.has_key(ALERT_EMERGS):
                for alert in hangseng_data[ALERT_EMERGS]:
                    if len(hangseng_data[ALERT_EMERGS][alert]) > 0:
                        score = -2
            elif hangseng_data.has_key(ALERT_WARNS):
                for alert in hangseng_data[ALERT_WARNS]:
                    if len(hangseng_data[ALERT_WARNS][alert]) > 0:
                        score = -1
        return score


    def readDataToday(self, collection):
        hangseng_datas = self.mongo_helper.find(collection, {"date":self.today})
        if hangseng_datas:
            return hangseng_datas[0]
        else:
            return {}

if __name__ == "__main__":
    alert_summary = AlertSummary()
    score = alert_summary.getScoreToday() 
    dingtalker = DingTalkSender()
    dingtalker.sendText("%d %s" % (score, "http://47.103.104.36/report"))
