#!coding=utf-8
import requests
import os
import re
import json
import datetime
import time
import pandas as pd
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import win32api, win32con


def raw(text):  # 转化URL字符串

    escape_dict = {
        '/': '%252F',
        '?': '%253F',
        '=': '%253D',
        ':': '%253A',
        '&': '%26',

    }
    new_string = ''
    for char in text:
        try:
            new_string += escape_dict[char]
        except KeyError:
            new_string += char
    return new_string


def mmm(item, id):
    item = raw(item)
    url = 'https://apapia.manmanbuy.com/ChromeWidgetServices/WidgetServices.ashx'
    s = requests.session()
    headers = {
        'Host': 'apapia.manmanbuy.com',
        'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
        'Proxy-Connection': 'close',
        'Cookie': 'ASP.NET_SessionId=uwhkmhd023ce0yx22jag2e0o; jjkcpnew111=cp46144734_1171363291_2017/11/25',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_3 like Mac OS X) AppleWebKit/603.3.8 (KHTML, like Gecko) Mobile/14G60 mmbWebBrowse',
        'Content-Length': '457',
        'Accept-Encoding': 'gzip',
        'Connection': 'close',
    }
    postdata = 'c_devid=2C5039AF-99D0-4800-BC36-DEB3654D202C&username=&qs=true&c_engver=1.2.35&c_devtoken=&c_devmodel=iPhone%20SE&c_contype=wifi&' \
               't=1537348981671&c_win=w_320_h_568&p_url={}&' \
               'c_ostype=ios&jsoncallback=%3F&c_ctrl=w_search_trend0_f_content&methodName=getBiJiaInfo_wxsmall&c_devtype=phone&' \
               'jgzspic=no&c_operator=%E4%B8%AD%E5%9B%BD%E7%A7%BB%E5%8A%A8&c_appver=2.9.0&bj=false&c_dp=2&c_osver=10.3.3'.format(
        item)
    s.headers.update(headers)
    req = s.get(url=url, data=postdata, verify=False).text

    print(req)
    try:
        js = json.loads(req)
        title = js['single']['title']  ##名称
    except Exception as e:
        print(e)
        # exit(mmm(item))
    ###数据清洗
    print(js)
    pic = js['single']['smallpic']  ##图片
    jiagequshi = js['single']['jiagequshi']  ##价格趋势
    lowerPrice = js['single']['lowerPrice']  ##最低价格
    lowerDate = js['single']['lowerDate']  ##最低价格日期
    lowerDate = re.search('[1-9]\d{0,9}', lowerDate).group(0)
    # print(lowerDate)
    lowerDate = time.strftime("%Y-%m-%d", time.localtime(int(lowerDate)))
    itemurl = js['single']['url']  ##商品链接
    qushi = js['single']['qushi']  ##趋势
    changPriceRemark = js['single']['changPriceRemark']  ##趋势变动
    date_list = []  ##日期
    price_list = []  ##价格
    print(jiagequshi)
    datalist = jiagequshi.replace('[Date.UTC(','').replace(')','').replace(']','').split(',')
    print("时间曲线：{}".format(datalist))

    for i in range(0, len(datalist), 5):
        day = int(datalist[i + 2])
        mon = int(datalist[i + 1])
        year = int(datalist[i])
        date = datetime.date(year=year, month=mon, day=day)
        date = date - datetime.timedelta(days=1)
        price = float(datalist[i + 3])
        date_list.append(date)
        price_list.append(price)
    print(date_list)
    print(price_list)

    data = {'date': date_list, 'price': price_list}
    df = pd.DataFrame(data)
    '''
    df.loc[:, "title_名称"] = title
    df.loc[:, "pic_图片"] = pic
    df.loc[:, "lowerPrice_最低价格"] = lowerPrice
    df.loc[:, "lowerDate_最低价格日期"] = lowerDate
    df.loc[:, "itemurl_商品链接"] = itemurl
    df.loc[:, "qushi_趋势"] = qushi
    df.loc[:, "changPriceRemark_趋势变动"] = changPriceRemark
    '''

    df.to_csv(str(id)+'.csv', index=False, mode='a', encoding="GB18030")  ##保存数据
    # print(df)
    # return df


if __name__ == '__main__':
    data = pd.read_csv(r'earphone.csv', encoding="utf-8")
    print(data.columns)
    data_url = data['url']
    flag = 0
    for i in data_url:
        print(i)
        item = i
        id = data.loc[:, 'id'].iloc[flag]
        mmm(item, id)
        flag += 1
    #item = 'https://detail.tmall.com/item.htm?id=538801983798'  ##京东、淘宝、天猫等电商平台数据都可以获取
    #item = 'https://chaoshi.detail.tmall.com/item.htm?id=615261692063&spm=875.7931836/B.2017039.4.42734265e60cRk&scm=1007.12144.81309.73136_0_0&pvid=a0ee91c8-881a-43f2-8929-aea7bff85c11&utparam=%7B%22x_hestia_source%22:%2273136%22,%22x_object_type%22:%22item%22,%22x_hestia_subsource%22:%22default%22,%22x_mt%22:0,%22x_src%22:%2273136%22,%22x_pos%22:1,%22wh_pid%22:-1,%22x_pvid%22:%22a0ee91c8-881a-43f2-8929-aea7bff85c11%22,%22scm%22:%221007.12144.81309.73136_0_0%22,%22x_object_id%22:615261692063,%22tpp_buckets%22:%222144#0#81309#96%22%7D'