#!/bin/python
# -*- coding: utf-8 -*-

import urllib
#sudo pip install beautifulsoup4
from bs4 import BeautifulSoup
import datetime
import os
import time
import sys
import random
import traceback

sys.path.append("%s/../" % os.path.dirname(os.path.abspath(__file__)))
print(sys.path)

from mongoHelper import MongoHelper
import logger

class HangsengIndex:
    def __init__(self):
        self.html = ""
        self.indexs = {}
        self.date = datetime.date.today().strftime("%Y%m%d")
        self.mongo_helper = MongoHelper("127.0.0.1", "stock")

    def curl_hangseng_index_sina_simple(self):
        url = "http://hq.sinajs.cn/list=int_hangseng"
        raw = urllib.urlopen(url)
        dclose,_,percent = raw.readline().split('"')[1].split(",")[1:4]
        dclose = float(dclose)
        percent = float(percent)
        logger.info_print("date(%s) dclose(%f) percent(%f)" % (self.date, dclose, percent))
        data = {
            "date": self.date,
            "dclose": dclose, 
            "percent": percent
        }
        self.mongo_helper.update("hangseng_index", {"date":self.date}, data, True)

    def to_float(self, s):
        return float(s.replace(",", ""))


    def curl_hangseng_index_yahoo(self):
        self.url = "https://hk.finance.yahoo.com/quote/%5EHSI/history?ltr=1&guccounter=1&guce_referrer=aHR0cHM6Ly94dWVxaXUuY29tL1MvSEtIU0k&guce_referrer_sig=AQAAAGtP5FNuYYONKlKt1JtDLAgcUo-MVNSIxtMO_BxUBIFKPizNuHf4vtkm02FxryW_4EUcsB8rGo_U6uh7ZKrhB_uCdnbHa_3uduuzCYCrACfVPPBgD5AyoZ5LecKNdeVKOv9sRpvXyaMuruL3J-GFKBSIHYxmJEwnrZR5rrhiFMR9"
        for line in urllib.urlopen(self.url):
            # grep 日期 | grep tbody | sed -e "s@</tr>@\n@g" | grep 年 | grep 月 | grep 日
            tbody_start = line.find("<tbody")
            if line.find("日期") >= 0 and tbody_start >= 0:
                tbody_stop=line.find("</tbody>")
                if tbody_stop < 0:
                    logger.warn_print("no </tbody> found")
                    continue
                tbody_stop += len("</tbody>")
                line = line[tbody_start:tbody_stop]
                #print("line: %s" % line)

                table=BeautifulSoup(line, "html.parser")
                for tr in table.find_all('tr'):
                    #print(">>>> ")
                    # 日期    開市    最高    最低    收市*    經調整收市價**    成交量
                    #for span in bsO.find_all('span'):
                    #    print(span.string)
                    datas = tr.find_all('span')
                    if len(datas) >= 5:
                        date= time.strftime("%Y%m%d", time.strptime(datas[0].string.encode("utf-8"), "%Y年%m月%d日"))
                        dopen = self.to_float(datas[1].string)
                        dmax = self.to_float(datas[2].string)
                        dmin = self.to_float(datas[3].string)
                        dclose = self.to_float(datas[4].string)
                        volume = self.to_float(datas[6].string) if len(datas) > 6 else 0
                        #print("%s %s %s %s %s %s" % (date, dopen, dmax, dmin, dclose, volume))
                        data={
                            "date":date, 
                            "dopen":dopen, 
                            "dmax":dmax, 
                            "dmin":dmin, 
                            "dclose":dclose, 
                            "volume":volume
                        }
                        self.mongo_helper.update("hangseng_index", {"date":date}, data, True)
            #            print(data)
    
if __name__ == "__main__":
    retry=0
    while (retry < 10):
        try:
            hangseng_index = HangsengIndex()
            #hangseng_index.curl_hangseng_index_sina_simple()
            hangseng_index.curl_hangseng_index_yahoo()
            logger.info("crawler/hangseng.py success, retry(%d)" % (retry))
            sys.exit(0)
        except Exception as e:
            tb = traceback.format_exc()
            logger.error("crawler/hangseng.py catch exception: %s, retry(%d) traceback(%s)" % (str(e), retry, tb))
            retry += 1
            time.sleep(random.randint(10, 60))
