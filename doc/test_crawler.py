#! /usr/bin/env python
#encoding:utf-8

import sys
reload (sys)
sys.setdefaultencoding('utf-8')

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait 

#PhantomJS动作函数
def Phantomjs_Get_WebPage(a,b,c):

    #通过Selenium构造PhantomJS浏览器
    print 'PhantomJS Browser Structing ...\n'
    browser=webdriver.PhantomJS()

    print 'Opening Original Website....\n'
    url='这里填入你的URL'
    browser.get(url)

    #填写a并确认
    browser.find_element_by_xpath('xpath_a').clear()
    browser.find_element_by_xpath('xpath_a').send_keys(a)
    browser.find_element_by_xpath('xpath_a').click()

    #填写b并确认
    browser.find_element_by_xpath('xpath_b').clear()
    browser.find_element_by_xpath('xpath_b').send_keys(b)
    browser.find_element_by_xpath('xpath_b').click()

    #填写c
    browser.find_element_by_xpath('xpath_c').clear()
    browser.find_element_by_xpath('xpath_c').send_keys(c)

    #提交确认
    browser.find_element_by_xpath('xpath_d').click()

    if(YorN_Xpath(browser,wait_time=10,xpath_Probe="xpath_e")):

        webpage_sourcecode=browser.find_element_by_xpath('//*').get_attribute('outerHTML')
        #webpage_sourcecode是unicode
        browser.quit()#请求完直接断开和目标网站链接,充分利用提取和存库的时间

        #Extract和save两个函数分别是提取和入库的函数，这里没有给出来，在提取和入库博文的时候再给出来吧
        extracted_Data_singlePage=Extract(webpage_sourcecode,a,b)
        save(extracted_Data_singlePage,a,b) 

        return True


    else:
        print '请求AJAX超时'
        browser.quit()

        return False


#AJAX是否加载成功的判断函数
def YorN_Xpath(browser,wait_time=10,xpath_Probe):

    try:
        wait_for_ajax_element=WebDriverWait(browser,wait_time)#10秒内每隔500ms扫描一次页面变化
        wait_for_ajax_element.until( lambda  the_driver:the_driver.find_element_by_xpath(xpath_Probe).is_displayed())
        print '获取AJAX数据成功\n'

        return True

    except:

        print '获取AJAX数据失败\n'

        return False
