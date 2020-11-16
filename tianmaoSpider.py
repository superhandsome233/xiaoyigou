from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

url = "https://chaoshi.detail.tmall.com/item.htm?id=622071272568"
#chrome_options = Options()
#chrome_options.add_argument('--headless')
#chrome_options.add_argument('--disable-gpu')
driver = webdriver.Chrome()#chrome_options=chrome_options
driver.get(url)
print(driver.page_source)
'''

usr = driver.find_element_by_xpath("//div[@class='input-plain-wrap input-wrap-loginid']//input")
pwd = driver.find_element_by_xpath("//div[@class='input-plain-wrap input-wrap-password']//input")
time.sleep(0.5)
usr.send_keys("")
time.sleep(0.5)
pwd.send_keys("")
submit = driver.find_element_by_class_name("fm-button fm-submit password-login")
submit.click()
time.sleep(0.5)

'''
driver.add_cookie({"name":"JSESSIONID","value":"10CE271BE1C35FA5EAF4688866B6C5B7"})
time.sleep(1)
driver.refresh()
time.sleep(1)
# html = driver.page_source
price = driver.find_element_by_xpath("//div[@id='detail']//span[@class='tm-price']").text
comment = driver.find_element_by_xpath("//div[@id='J_Detail']//div[@class='rate-score']/strong").text
tags = driver.find_elements_by_xpath("//div[@id='J_Detail']//div[@class='rate-tag-inner']//span")
for tag in tags:
    Tag = tag.text
    print(Tag)
    print("\n")
print("价格为{},好评率为{}".format(price,comment))
# time.sleep(4)

driver.quit()