#! /usr/local/bin/python
# encoding: utf-8
 
'''
@author: wulinfeng
@date: 2018-1-5
'''
 
import time
#import request
from selenium import webdriver
#from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
 
def init_web_driver():
    global DRIVER
    
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    
    DRIVER = webdriver.Chrome(chrome_options=chrome_options)
    
def close_web_driver():
    DRIVER.quit() 
    
def get_data():
    #url = "https://hk.finance.yahoo.com/quote/%5EHSI/history?ltr=1&guccounter=1&guce_referrer=aHR0cHM6Ly94dWVxaXUuY29tL1MvSEtIU0k&guce_referrer_sig=AQAAAGtP5FNuYYONKlKt1JtDLAgcUo-MVNSIxtMO_BxUBIFKPizNuHf4vtkm02FxryW_4EUcsB8rGo_U6uh7ZKrhB_uCdnbHa_3uduuzCYCrACfVPPBgD5AyoZ5LecKNdeVKOv9sRpvXyaMuruL3J-GFKBSIHYxmJEwnrZR5rrhiFMR9"
    #url = "https://hk.finance.yahoo.com/quote/9988.HK/history?period1=1576425600&period2=1576598400&interval=1d&filter=history&frequency=1d"
    url="https://ha.emas.alibaba-inc.com/api/v1/crash/converge/list/grid?version=9.6.1&begin=1587713809601&end=1587713809601&errorType=ANDROID_NATIVE_CRASH&keyword=&clusterType=ALL&selectedTags=&appId=12278902@android&selectBundleName=dai,alinnpython&bizBundleName=&pageNo=1&pageSize=10"
    print DRIVER.get(url)
    #tds = DRIVER.find_element_by_xpath("//table//tbody").find_elements_by_tag_name("td")
    #for td in tds:
    #    print(td.text)
    
    
    
init_web_driver()
get_data()
close_web_driver()
