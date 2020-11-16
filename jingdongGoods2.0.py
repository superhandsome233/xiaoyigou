# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd


def process(url,i):
    #chrome_options = Options()
    #chrome_options.add_argument('--headless')
    #chrome_options.add_argument('--disable-gpu')
    driver = webdriver.Chrome()  #chrome_options=chrome_options
    driver.get(url)
    # driver.get("https://item.jd.com/72387612352.html")
    time.sleep(4)

    price = driver.find_element_by_xpath("//span[@class='p-price']").text
    button = driver.find_element_by_xpath("//div[@class='detail']//div[@class='ETab']//div[@class='tab-main large']//li[position()=5]")
    button.click()
    time.sleep(6)
    if driver.find_element_by_xpath("//div[@class='detail']//div[@class='m m-content comment']//div[@class='mc']").text == "暂无评价":
        comment = driver.find_element_by_xpath("//div[@class='detail']//div[@class='m m-content comment']//div[@class='mc']").text
    else:
        comment = driver.find_element_by_xpath("//div[@class='percent-con']").text
    tags = driver.find_elements_by_xpath("//div[@class='percent-info']")
    sell = driver.find_element_by_xpath("//div[@class='detail']//div[@class='ETab']//div[@class='tab-main large']//li[position()=5]//s").text

    data.loc[:, 'price_价格'].iloc[i] = price
    data.loc[:, 'feedback_好评率'].iloc[i] = comment
    for tag in tags:
        data.loc[:, 'tag_标签'].iloc[i] = tag
    data.loc[:, 'sell_销量'].iloc[i] = sell
    time.sleep(2)
    driver.quit()


data = pd.read_csv(r'calculator.csv',encoding="gbk")
data_url = data['itemurl_商品链接']
i = 0
for url in data_url:
    process(url, i)
    i += 1
    time.sleep(10)
data.to_csv(r'calculator.csv',encoding="gbk")
print("successfully!")