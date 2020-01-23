import sys
import datetime
import json
import re

def compare_array(ax, ay):
    if len(ax) != len(ay):
        return False 
    for i in range(len(ax)):
        if type(ax[i]) != type(ay[i]):
            return False
        if isinstance(ax[i], float):
            if abs(ax[i]-ay[i]) > 0.001:
                return False
        elif ax[i] != ay[i]:
            return False
    return True

def getYesterday():
    today=datetime.date.today()
    oneday=datetime.timedelta(days=1)
    yesterday=today-oneday
    return yesterday.strftime("%Y%m%d")

def getToday():
    today=datetime.date.today()
    return today.strftime("%Y%m%d")

def getFormalCode(code):
    return "c%s" % code.replace(".", "").replace("^", "").strip()


def parseConfigSubject(subject_pathfile):
    config = []
    for subject in open(subject_pathfile, "r"):
        items = subject.split()
        if len(items) >= 2:
            code, name = items
        if len(items) == 1:
            code = name = items[0]
        formalCode = getFormalCode(code)
        config.append({"code":code, "fcode":formalCode, "name":name.decode("utf-8")})
    return config

def parseCustomWarns(customWarns_pathfile):
    custom_warns_list = []
    with open(customWarns_pathfile, "r") as f:
        custom_warns_list = json.load(f)
        assert isinstance(custom_warns_list, list)

    custom_warns = {}
    for warn in custom_warns_list:
        assert warn.get("subject") and warn.get("rule") and warn.get("warn")
        warn_id = getFormalCode(warn.get("subject"))+"_"+warn.get("rule")
        custom_warns[warn_id] = warn
    return custom_warns

def parseRuleConfig(rule_pathfile):
    with open(rule_pathfile, "r") as f:
        s = f.read()
        pattern=re.compile(r"#.*\n")
        conf = re.sub(pattern, "\n", s)
        return json.loads(conf)
    return None



if __name__ == '__main__':
    for tuples in parseConfigSubject("config/subjects.conf"):
        print tuples["code"], tuples["fcode"], tuples["name"]
    
    print parseCustomWarns("config/custom_warns")
