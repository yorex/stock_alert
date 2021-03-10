# coding=utf-8

import sys
import os
sys.path.append("../")
from engine import RuleEngine
from utils import getToday
from dingtalk_sender import DingTalkSender
import json
import time

old_rt_warns_file="./.old_rt_warns"

def readFile(filepath):
    if not os.path.exists(filepath):
        return None
    with open(filepath, "r") as f:
        return f.read()

def writeFile(filepath, content):
    with open(filepath, "w") as f:
        f.write(content)

def getNminCount():
    n = 7200
    return str(int(time.time())/n);

if __name__ == "__main__":
    ruleEngine = RuleEngine()
    ruleEngine.load("../config/rules.conf", "../config/subjects_rt.conf", "../config/custom_warns")
    all_warns_ret = ruleEngine.run_for_date(getToday())
    if all_warns_ret:
        old_warns_str = readFile(old_rt_warns_file)
        new_warns_str=json.dumps(all_warns_ret)
        if old_warns_str != getNminCount()+":"+new_warns_str:
            writeFile(old_rt_warns_file, getNminCount()+":"+new_warns_str)
            dingtalker = DingTalkSender()
            dingtalker.sendText("realtime:\n---------\n %s" % "\n---------\n".join(all_warns_ret))
        else:
            print "warns is same, ignore"
