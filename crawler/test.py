#! /usr/bin/env python
#encoding:utf-8

import sys
reload (sys)
sys.setdefaultencoding('utf-8')

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait 
import phantomjs_bin

sys.path.append(phantomjs_bin.executable_path)
print sys.path

#PhantomJS动作函数
def Phantomjs_Get_WebPage():

    #通过Selenium构造PhantomJS浏览器
    print 'PhantomJS Browser Structing ...\n'
    browser=webdriver.PhantomJS()

    print 'Opening Original Website....\n'
    url = "https://hk.finance.yahoo.com/quote/%5EHSI/history?ltr=1&guccounter=1&guce_referrer=aHR0cHM6Ly94dWVxaXUuY29tL1MvSEtIU0k&guce_referrer_sig=AQAAAGtP5FNuYYONKlKt1JtDLAgcUo-MVNSIxtMO_BxUBIFKPizNuHf4vtkm02FxryW_4EUcsB8rGo_U6uh7ZKrhB_uCdnbHa_3uduuzCYCrACfVPPBgD5AyoZ5LecKNdeVKOv9sRpvXyaMuruL3J-GFKBSIHYxmJEwnrZR5rrhiFMR9"
    browser.get(url)


    if YorN_Xpath(browser,xpath_Probe="//tr",wait_time=10):
        print "find xpath"

        webpage_sourcecode=browser.find_element_by_xpath('//*').get_attribute('outerHTML')
        #webpage_sourcecode是unicode
        browser.quit()#请求完直接断开和目标网站链接,充分利用提取和存库的时间

        print(webpage_sourcecode)

        #Extract和save两个函数分别是提取和入库的函数，这里没有给出来，在提取和入库博文的时候再给出来吧
        #extracted_Data_singlePage=Extract(webpage_sourcecode,a,b)
        #save(extracted_Data_singlePage,a,b) 

        return True


    else:
        print '请求AJAX超时'
        browser.quit()

        return False


#AJAX是否加载成功的判断函数
def YorN_Xpath(browser,xpath_Probe,wait_time=10):

    try:
        wait_for_ajax_element=WebDriverWait(browser,wait_time)#10秒内每隔500ms扫描一次页面变化
        wait_for_ajax_element.until( lambda  the_driver:the_driver.find_element_by_xpath(xpath_Probe).is_displayed())
        print '获取AJAX数据成功\n'

        return True

    except:

        print '获取AJAX数据失败\n'

        return False


if __name__ == "__main__":
    Phantomjs_Get_WebPage()
