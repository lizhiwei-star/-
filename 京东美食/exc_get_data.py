# from selenium import webdriver
# import time


# # driver = webdriver.Chrome()     # 创建Chrome对象.
# driver = webdriver.Chrome("C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe")
# # 操作这个对象.
# driver.get('https://www.baidu.com')     # get方式访问百度.
# time.sleep(2)
# driver.quit()   # 使用完, 记得关闭浏览器, 不然chromedriver.exe进程为一直在内存中.


# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.support.wait import WebDriverWait

# driver = webdriver.Chrome("C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe")
# driver.maximize_window()	# 浏览器最大化
# driver.set_window_size(480, 800)	# 设置浏览器480,800为像素大小
# driver.minimize_window()	# 浏览器最小化
# driver.refresh()         # 浏览器刷新，与F5同理
# try:
#     driver.get('https://www.baidu.com')
#     input = driver.find_element_by_id('kw')
#     input.send_keys('Python') 	 
#     input.send_keys(Keys.ENTER)
#     driver.back()			 # 后退到上一个页面
#     driver.forward()		 # 前进到下一个页面
#     wait = WebDriverWait(driver, 10)
#     wait.until(EC.presence_of_element_located((By.ID, 'content_left')))
#     print(driver.current_url)
#     print(driver.get_cookies())
#     print(driver.page_source)
# finally:
#     driver.close()			 # 关闭当前窗口，不会关闭浏览器驱动
#     driver.quit()			 # 退出所有窗口并关闭浏览器驱动

# # 先清空，再在百度搜索框中输入“测试”
# driver.find_element_by_id('kw').clear()
# driver.find_element_by_id('kw').send_keys('测试')

# # 京东页面底部有很多链接，通过此属性滚动到该元素所在的位置
# driver.find_element_by_link_text('合作招商').location_once_scrolled_into_view 



from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from urllib.parse import quote
from pyquery import PyQuery as pq
import pymongo
import time
from selenium.webdriver.common.action_chains import ActionChains
import pymysql
from pymysql import escape_string
import pandas as pd
import numpy as np
import re

MAX_PAGE = 40
MONGO_URL = 'localhost'
MONGO_DB = 'taobao'
MONGO_COLLECTION = 'foods'
client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]

browser = webdriver.Chrome("C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe")
wait = WebDriverWait(browser, 10)
KEYWORD='美食'

def index_page():
    """
    抓取索引页：param page：页码
    """
    
    for i in range(1, MAX_PAGE+1):
        page=i
        print('正在爬取第', page, '页')
        try:
            if page==1:
                url = 'https://search.jd.com/Search?keyword=' + quote(KEYWORD) + '&enc=utf-8&wq=m&pvid=20032098857046f5b9466fea79984bdf'
                browser.get(url)
                browser.maximize_window()
            if  page < 99:
                input = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '#J_bottomPage span.p-skip > input')))
                
                # submit = wait.until(
                # EC.element_to_be_clickable((By.CSS_SELECTOR, '#J_bottomPage span.p-skip > a.btn.btn-default')))
                # ActionChains(browser).double_click(input).perform()
                # js = 'document.querySelector("#kw").value="";'
                # browser.execute_script(js)
                # input.click()
                # input.clear()
                # input.send_keys('2')
                # time.sleep(3)
                
                # wait.until(
                # EC.text_to_be_present_in_element((By.CSS_SELECTOR, '#J_bottomPage a.curr'), str(page)))
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#J_goodsList .gl-i-wrap')))
                get_products()
                submit = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '#J_topPage a.fp-next')))
                submit.click()
        except TimeoutException:
            index_page(page)

def get_products():
    '''
    提取商品
    '''
    html = browser.page_source
    doc = pq(html)
    items = doc('#J_goodsList div.gl-i-wrap').items()
    for item in items:
        product = {
        'image': item.find('div.p-img').attr('data-src'), 
        'price': item.find('div.p-price').text(),  
        'deal': item.find('div.p-name.p-name-type-2').text(),  
        'commit_num': item.find('div.p-commit').text(),  
        'shop': item.find('div.p-shop').text(),  
        'location': item.find('div.p-icons').text()
        }
        print(product)
        
        sql=f'''insert into jd(image,price,deal,commit_num,shop,location) values('{product['image']}','{product['price']}','{escape_string(product['deal'])}','{escape_string(product['commit_num'])}','{product['shop']}','{product['location']}')'''
        cursor.execute(sql)
        coon.commit()
 
def main():
    '''
    遍历每一页
    '''
    for i in range(1, MAX_PAGE+1):
        index_page(i)
    # browser.close()
 
def save_to_mongo(result):
    """
    保存至MongoDB
    """
    try:
        if db[MONGO_COLLECTION].insert(result):
            print('存储到MongoDB 成功')
    except Exception:  
        print('存储到MongoDB失败')
 
if __name__ == '__main__':
    coon = pymysql.connect(
    host='localhost', user='root', passwd='',
    port=3306, db='fff', charset='utf8'
    # port必须写int类型
    # charset必须写utf8，不能写utf-8
    )
    cursor = coon.cursor()
    index_page()
