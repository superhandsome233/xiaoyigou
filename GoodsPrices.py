import urllib.request
from bs4 import BeautifulSoup
# 爬取的网址是在京东商城上，以书包为关键词搜索，爬取了页面上书包的商品名称和价格
headers = {"User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 6.0 x64; en-US; rv:1.9pre) Gecko/2008072421 Minefield/3.0.2pre"}
url = "https://search.jd.com/Search?keyword=%E4%B9%A6%E5%8C%85&enc=utf-8&pvid=ef555c7a0f254824b71b1c334e44ee2e"
req=urllib.request.Request(url,headers=headers)
data=urllib.request.urlopen(req)
data=data.read()
soup=BeautifulSoup(data,"lxml")
Goods=soup.select("ul[class='gl-warp clearfix'] li[class='gl-item']")
print("序号    价格    商品名称")
num=0
for goods in Goods:
    try:
        num=num+1
        name=goods.select('div[class="p-name p-name-type-2"] em')[0].text
        price=goods.select('div[class="p-price"] i')[0].text
        print("{:<5}{:^10}{:>40}".format(num, price, name.replace('\n', '').replace('\r', '')))
    except IndexError:
        pass