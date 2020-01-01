from dingtalk_sender import DingTalkSender
from mongoHelper import MongoHelper
import time
import json
import sys
import datetime
import logger

ALERT_WARNS="alert_warns"
ALERT_EMERGS="alert_emergs"

def getYesterday(): 
    today=datetime.date.today() 
    oneday=datetime.timedelta(days=1) 
    yesterday=today-oneday  
    return yesterday.strftime("%Y%m%d")


class AlertSummary:
    def __init__(self, date=None):
        self.mongo_helper = MongoHelper("stock")
        if date:
            self.date = date
        else:
            self.date = getYesterday()
        self.collections = ["hangseng_index"]
        for subject in  open("config/subjects.conf", "r"): 
            subject="c%s" % subject.replace(".", "").strip()
            self.collections.append(subject)

    def generateSummary(self):
        content = [self.date]
        for collection in self.collections:
            collcont =  {}
            hangseng_data = self.readData(collection)
            if hangseng_data.has_key(ALERT_EMERGS):
                collcont[collection+"-"+ALERT_EMERGS] = hangseng_data[ALERT_EMERGS]
            if hangseng_data.has_key(ALERT_WARNS):
                collcont[collection+"-"+ALERT_WARNS] = hangseng_data[ALERT_WARNS]
            if hangseng_data.has_key("warn"):
                collcont[collection+"-warn"] = hangseng_data["warn"]
            if collcont:
                content.append(collcont)
        return content


    def getScore(self):
        score = 0
        for collection in self.collections:
            hangseng_data = self.readData(collection)
            if hangseng_data.has_key(ALERT_EMERGS):
                for alert in hangseng_data[ALERT_EMERGS]:
                    if len(hangseng_data[ALERT_EMERGS][alert]) > 0:
                        score = -2
            elif hangseng_data.has_key(ALERT_WARNS):
                for alert in hangseng_data[ALERT_WARNS]:
                    if len(hangseng_data[ALERT_WARNS][alert]) > 0:
                        score = -1
        return score


    def readData(self, collection):
        hangseng_datas = self.mongo_helper.find(collection, {"date":self.date})
        logger.info_print("data: %s", hangseng_datas)
        if hangseng_datas:
            return hangseng_datas[0]
        else:
            return {}

if __name__ == "__main__":
    date = getYesterday()
    if len(sys.argv) > 1:
        date = sys.argv[1]
#    date='20190828'
    alert_summary = AlertSummary(date)
    score = alert_summary.getScore() 
    dingtalker = DingTalkSender()
    dingtalker.sendText("%d %s?date=%s" % (score, "http://47.103.104.36/report", date))
    alert_summary.generateSummary()
