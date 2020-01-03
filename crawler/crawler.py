#! /usr/local/bin/python
# encoding: utf-8

import time
import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import sys; sys.path.append("../")
from mongoHelper import MongoHelper
from utils import parseConfigSubject
import logger


class YahooCrawler:
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        self.DRIVER = webdriver.Chrome(chrome_options=chrome_options)
        self.mongo = MongoHelper("stock")

    def __del__(self):
        self.DRIVER.quit()

    def to_float(self, s):
        return float(s.replace(",", ""))

    def _save_data(self, fcode, datas):
        try:
            logger.info("save_data:%s", datas)
            date= time.strftime("%Y%m%d", time.strptime(datas[0].encode("utf-8"), "%Y年%m月%d日"))
            dopen = self.to_float(datas[1])
            dmax = self.to_float(datas[2])
            dmin = self.to_float(datas[3])
            dclose = self.to_float(datas[4])
            volume = self.to_float(datas[5])
            data={
                "date":date, 
                "dopen":dopen, 
                "dmax":dmax, 
                "dmin":dmin, 
                "dclose":dclose, 
                "volume":volume
            }
            collectionName = fcode
            if self.mongo.find(collectionName, {"date": date}).count() == 0:
                self.mongo.insert(collectionName, data)
                #self.mongo.update(collectionName, {"date":date}, data, True)
        except Exception as e:
            logger.error("save_data exception:%s", str(e))
    
    # 获取 [date_begin, date_end) 内的数据, date格式为%Y%m%d
    def fetch(self, subject, date_begin, date_end):
        epoch_begin = int(time.mktime(time.strptime(date_begin, "%Y%m%d")))
        epoch_end = int(time.mktime(time.strptime(date_end, "%Y%m%d")))
        url = "https://hk.finance.yahoo.com/quote/%s/history?period1=%s&period2=%s&interval=1d&filter=history&frequency=1d" % (subject["code"], epoch_begin, epoch_end)
        logger.info("url:%s", url)
        self.DRIVER.get(url)
        trs = self.DRIVER.find_element_by_xpath("//table//tbody").find_elements_by_tag_name("tr")
        for tr in trs:
            tds = tr.find_elements_by_tag_name("td")
            self._save_data(subject["fcode"], [td.text for td in tds])


if __name__ == "__main__":
    today = datetime.date.today()
    oneday = datetime.timedelta(days=30)
    yesterday = today - oneday
    tomorrow = today + oneday
    
    for subject in parseConfigSubject("../config/subjects.conf"):
        try:
            yahooCrawler = YahooCrawler();
            yahooCrawler.fetch(subject, yesterday.strftime("%Y%m%d"), tomorrow.strftime("%Y%m%d"));
            del yahooCrawler
        except Exception as e:
            logger.error("process subject(%s) exception:%s", subject["name"], str(e))

 
