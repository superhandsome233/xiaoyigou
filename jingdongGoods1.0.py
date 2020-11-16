from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
driver = webdriver.Chrome(chrome_options=chrome_options)#
#driver.get("https://www.miaomiaozhe.com/jump?gid=-1136548399250300628&url=519B671A0B977Ff92wOtH1SIhBGZt1TgrzlBTeLyNuTIXic5sSC_eu9tPRdsxyzYq5K5Aqb")
driver.get("https://item.jd.com/72387612352.html")
# html = driver.page_source
time.sleep(3)
price = driver.find_element_by_xpath("//span[@class='p-price']").text
print("价格：{}".format(price))
button = driver.find_element_by_xpath("//li[@clstag='shangpin|keycount|product|shangpinpingjia_2']")
#time.sleep(1)
button.click()
time.sleep(6)
comment = driver.find_element_by_xpath("//div[@class='percent-con']").text  #//div[@class='detail']//div[@class='m m-content comment']
print("好评率：{}".format(comment))
tags = driver.find_elements_by_xpath("//div[@class='percent-info']")
flag = 1
for tag in tags:
    if(flag):
        print("标签：{}".format(tag.text))
        flag = 0
    else:
        print(tag.text)
sell = driver.find_element_by_xpath("//div[@class='J-comments-list comments-list ETab']//a[@clstag='shangpin|keycount|product|allpingjia_tuijianpaixu_eid=100^^tagid=ALL^^pid=20022^^sku=14754765989^^sversion=1001^^pageSize=1']//em").text
print("销量：{}".format(sell))

# time.sleep(4)
driver.quit()