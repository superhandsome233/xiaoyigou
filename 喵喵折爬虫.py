from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import time
import csv
import pandas as pd
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyquery import PyQuery as pq
import os
def get_good(name):
        driver = webdriver.Chrome()

        driver.get('https://www.miaomiaozhe.com/search?q='+name)
        wait = WebDriverWait(driver, 100)
        js_code = '''
                         paras = document.getElementsByClassName('panel panel-figure hot-click');
        for(i=0;i<paras.length;i++){
            //删除元素 元素.parentNode.removeChild(元素);
            if (paras[i] != null) 
          paras[i].parentNode.removeChild( paras[i]); 
}                      
                                            '''
        driver.execute_script(js_code)
        cnt=3
        while(cnt):
            driver.execute_script('window.scrollTo(0, 1*document.body.scrollHeight)')
            cnt=cnt-1
            time.sleep(3)
        goodList = []
        wait.until(EC.presence_of_element_located((By.CLASS_NAME,"item.cl")))
        # 商品详情wrap
        good_list = driver.find_elements_by_class_name('item.cl')
        for good in good_list:
            # 商品名称
            goods_name = good.find_element_by_class_name('title').text.replace("\n", " ")
            # 商品图片
            goods_picture = good.find_element_by_css_selector('img').get_attribute('src')
            # # 商品价格
            # goods_price = good.find_element_by_css_selector('strong').text.replace("\n", " ")
            # 商品链接
            goods_link = good.find_element_by_css_selector('a.btn').get_attribute('href')
            # print(goods_price)
            good_content = {
                    "商品名称": goods_name,
                    "商品图片": goods_picture,
                    # "商品价格": goods_price,
                    "商品链接": goods_link
             }
            goodList.append(good_content)
        return goodList


if __name__ == '__main__':
    name = "耳机"
    good_list = get_good(name)
    header = ['商品名称','商品图片',"商品链接"]  # 数据列名

    # df = pd.read_csv('test.csv',encoding='utf-8')
    # df.drop(header,axis=1)
    # df.close()
    with open('test.csv', 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=header)  # 提前预览列名，当下面代码写入数据时，会将其一一对应。
        writer.writeheader()  # 写入列名
        writer.writerows(good_list)  # 写入数据
