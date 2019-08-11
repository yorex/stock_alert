#coding=utf8
import urllib2
import json

class DingTalkSender():
    def __init__(self):
        self.url = 'https://oapi.dingtalk.com/robot/send?access_token=857278ccfaf791efa64ebc9d19dfac88702bf3eed7632a920132506dae107c4a'

    def sendText(self, text):
        headers = {'Content-Type': 'application/json'}
        data = {"msgtype": "text" }
#        data = {
#            "msgtype": "text", 
#            "at": {
#                "isAtAll": True
#            }
#        }
        data["text"] = {"content": text}

        req = urllib2.Request(self.url, json.dumps(data), headers) 
        response = urllib2.urlopen(req) 
    

if __name__ == "__main__":
    dingtalker = DingTalkSender()
    dingtalker.sendText("hahahafsjfl 台风来了 ")
