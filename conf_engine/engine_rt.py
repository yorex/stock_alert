# coding=utf-8

import sys
sys.path.append("../")
from engine import RuleEngine
from utils import getToday
from dingtalk_sender import DingTalkSender

if __name__ == "__main__":
    ruleEngine = RuleEngine()
    ruleEngine.load("../config/rules.conf", "../config/subjects_rt.conf", "../config/custom_warns")
    all_warns_ret = ruleEngine.run_for_date(getToday())
    if all_warns_ret:
        dingtalker = DingTalkSender()
        dingtalker.sendText("realtime:\n %s" % all_warns_ret)
