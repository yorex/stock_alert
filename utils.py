import sys
import datetime

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


def parseConfigSubject(subject_pathfile):
    config = []
    for subject in open(subject_pathfile, "r"):
        items = subject.split()
        if len(items) >= 2:
            code, name = items
        if len(items) == 1:
            code = name = items[0]
        formalCode = "c%s" % code.replace(".", "").strip()
        config.append({"code":code, "fcode":formalCode, "name":name.decode("utf-8")})
    return config

if __name__ == '__main__':
    for tuples in parseConfigSubject("config/subjects.conf"):
        print tuples["code"], tuples["fcode"], tuples["name"]
    
