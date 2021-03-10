from dingtalk_sender import DingTalkSender
from mongoHelper import MongoHelper
import time
import json
import sys
import datetime
import logger
from utils import parseConfigSubject, getToday, getYesterday
from to_string import ToString

DEBUG=False

ALERT_WARNS="alert_warns"
ALERT_EMERGS="alert_emergs"

class AlertSummary:
    def __init__(self, date=None):
        self.mongo_helper = MongoHelper("stock")
#        self.collections = ["hangseng_index"]
        self.subjects = []
        for subject in parseConfigSubject("config/subjects.conf"):
            self.subjects.append(subject)

        if date:
            self.date = date
        else:
            self.date = self.getLatestDataDay(getToday())

    def generateTextSummary(self):
        stringer = ToString("utf-8")
        content = "Date: %s" % self.date

        for subject in self.subjects:
            data = self.readData(subject['fcode'])
            if data.has_key("warn"):
                content += "\n-------- %s --------\n" % subject['name']
                for ruleName in data['warn']:
                    content += "%-12s\t%s\n" % (ruleName, data["warn"][ruleName])
        return content
 

    def generateHtmlSummary(self):
        stringer = ToString("utf-8")
        content = ""
        content += """
    <style>
      table, th, td {
      padding: 10px;
      border: 1px solid black; 
      border-collapse: collapse;
      }
    </style>
    <style> 
     .hdc{ font-size:28px} 
     .tdc{ font-size:26px} 
    </style> 
            """

        for subject in self.subjects:
            content += "<h2 class=\"hdc\">%s</h2>" % subject['name']
            content += "<table>"
            data = self.readData(subject['fcode'])
            if data.has_key("warn"):
                for ruleName in data['warn']:
                    content += "<tr class=\"tdc\"><td>%s</td><td>%s</td></tr>" % (ruleName, data["warn"][ruleName])
            content += "</table>"
        return content
 

    def generateSummary(self):
        stringer = ToString("utf-8")
        content = [self.date]
#        for collection in self.collections:
#            collcont =  {}
#            hangseng_data = self.readData(collection)
#            if hangseng_data.has_key(ALERT_EMERGS):
#                collcont[collection+"-"+ALERT_EMERGS] = hangseng_data[ALERT_EMERGS]
#            if hangseng_data.has_key(ALERT_WARNS):
#                collcont[collection+"-"+ALERT_WARNS] = hangseng_data[ALERT_WARNS]
#            if collcont:
#                content.append(collcont)
        for subject in self.subjects:
            collcont =  {}
            data = self.readData(subject['fcode'])
            if data.has_key("warn"):
                collcont[subject['name']+"-warn"] = data["warn"]
            if collcont:
                content.append(collcont)
        # ok
        #return stringer.toString(content)

        ## not work
        #return json.dumps(content, ensure_ascii=False, indent=4, encoding="gbk")

        return content
    
    def getEvents(self):
        stringer = ToString("gbk")
        events = [];
#        for collection in self.collections:
#            hangseng_data = self.readData(collection)
#            if hangseng_data.has_key(ALERT_EMERGS):
#                for alert in hangseng_data[ALERT_EMERGS]:
#                    if len(hangseng_data[ALERT_EMERGS][alert]) > 0:
#                        events.append("hangseng_emerg") 
#                        break;
#            elif hangseng_data.has_key(ALERT_WARNS):
#                for alert in hangseng_data[ALERT_WARNS]:
#                    if len(hangseng_data[ALERT_WARNS][alert]) > 0:
#                        events.append("hangseng_warn") 
#                        break;
        for subject in self.subjects:
            data = self.readData(subject['fcode'])
            if data.has_key("warn"):
                events.append(subject['name'])
        return events
 

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
        if DEBUG:
            logger.info_print("data: %s", hangseng_datas)
        if hangseng_datas:
            return hangseng_datas[0]
        else:
            return {}

    def getLatestDataDay(self, date):
        collection = self.subjects[0]["fcode"]
        datas = self.mongo_helper.find(collection, {"date":{"$lte":date}})
        return datas[-1]["date"]

if __name__ == "__main__":
    date = None
    if len(sys.argv) > 1:
        date = sys.argv[1]
#    date='20190828'

    dingtalker = DingTalkSender()
    alert_summary = AlertSummary(date)

    if 0:
        events = alert_summary.getEvents() 
        dingtalker.sendText("%d %s %s?date=%s" % (len(events), str(events), "http://47.103.104.36/reportHtml", alert_summary.date))
    else:
        dingtalker.sendText(alert_summary.generateTextSummary())
    print alert_summary.generateTextSummary()
