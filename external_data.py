#!/bin/python
# -*- coding: utf-8 -*-

import urllib
#sudo pip install beautifulsoup4
from bs4 import BeautifulSoup

class HangsengIndex:
    def __init__(self):
        self.html = ""
        self.indexs = {}

    def curl_hangseng_index(self):
        self.url = "https://hk.finance.yahoo.com/quote/%5EHSI/history?ltr=1&guccounter=1&guce_referrer=aHR0cHM6Ly94dWVxaXUuY29tL1MvSEtIU0k&guce_referrer_sig=AQAAAGtP5FNuYYONKlKt1JtDLAgcUo-MVNSIxtMO_BxUBIFKPizNuHf4vtkm02FxryW_4EUcsB8rGo_U6uh7ZKrhB_uCdnbHa_3uduuzCYCrACfVPPBgD5AyoZ5LecKNdeVKOv9sRpvXyaMuruL3J-GFKBSIHYxmJEwnrZR5rrhiFMR9"
        data=[]
        for line in urllib.urlopen(self.url):
            # grep 日期 | grep tbody | sed -e "s@</tr>@\n@g" | grep 年 | grep 月 | grep 日
            if line.find("日期") > 0 and line.find("tbody") > 0:
                trs = line.split("</tr>")
                for tr in trs:
                    if tr.startswith("<tr class"):
                        bsO=BeautifulSoup(tr, "html.parser")
                        #print(">>>> ")
                        # 日期    開市    最高    最低    收市*    經調整收市價**    成交量
                        #for span in bsO.find_all('span'):
                        #    print(span.string)
                        datas = bsO.find_all('span')
                        if len(datas) >= 7:
                            date= datas[0].string
                            dopen = datas[1].string
                            dmax = datas[2].string
                            dmin = datas[3].string
                            dclose = datas[4].string
                            volume = datas[6].string
                            #print("%s %s %s %s %s %s" % (date, dopen, dmax, dmin, dclose, volume))
                            data.append({
                                "date":date, 
                                "dopen":dopen, 
                                "dmax":dmax, 
                                "dmin":dmin, 
                                "dclose":dclose, 
                                "volume":volume
                            })
        return data
    
if __name__ == "__main__":
    hangseng_index = HangsengIndex()
    hangseng_index.curl_hangseng_index()
