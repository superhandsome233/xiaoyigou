'''
爬取京东商品信息:
功能: 通过chromeDrive进行模拟访问需要爬取的京东商品详情页(https://item.jd.com/100003196609.html)并且程序支持多个页面爬取，输入时以逗号分隔，
思路: 创建webdriver对象并且调用get方法请求url,进入页面根据dom结构爬取一些简要信息，之后
通过模拟点击商品评价按钮，再分别解析没个用户的评价信息，到每页的底部时，模拟点击下一页按钮
获取新的一页数据。
    提取商品信息:
        商品名称: {goods_name}
        商品价格: {goods_price}
        好评度: {percent_con}
        评价标签: {tags}
        评价类型
        姓名：{username}
        星级：{star}
        文字：{word}
        评价图片: {picList}
        购买类型: {order_type}
        购买日期：{order_date}
        点赞人数： {likes}
        评论人数: {
'''
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import time
# 根据类名用来判断元素是否存在
def isElementPresent(driver, element):
        """
        用来判断元素标签是否存在，
        """
        try:
            driver.find_element_by_class_name(element)
        # 原文是except NoSuchElementException, e:
        except NoSuchElementException as e:
            # 发生了NoSuchElementException异常，说明页面中未找到该元素，返回False
            return False
        else:
            # 没有发生异常，表示在页面中找到了该元素，返回True
            return True
## 获取评价
def get_evaluation(goods_detail):
    js_code = '''
                                            window.scrollTo(0,2000);
                                        '''
    driver.execute_script(js_code)  # 执行js代码
    ## 评价详细信息
    try:
        comments = goods_detail.find_elements_by_class_name('comment-item')
        for comment in comments:
            picList = []
            username = comment.find_element_by_class_name('user-info').text.replace("\n", "")
            star = comment.find_element_by_class_name('comment-star').get_attribute('class')[-1] + '星级'
            word = comment.find_element_by_class_name('comment-con').text.replace("\n", "")
            # 调用isElementExist方法，判断元素是否存在
            flag = isElementPresent(comment, 'pic-list')
            if  flag:
                pics = comment.find_element_by_class_name('pic-list').find_elements_by_tag_name('a')
                for pic in pics:
                    picList.append(pic.find_element_by_tag_name('img').get_attribute('src'))
            order_type = comment.find_element_by_class_name('order-info').find_elements_by_tag_name('span')[0].text
            order_date = comment.find_element_by_class_name('order-info').find_elements_by_tag_name('span')[-1].text

            likes = comment.find_element_by_class_name('J-nice').text
            sprite_comment = comment.find_element_by_class_name('comment-op').find_elements_by_tag_name('a')[2].text
            goods_content = f'''    
                姓名：{username}
                星级：{star}
                文字：{word}
                评价图片: {picList}
                购买类型: {order_type}
                购买日期：{order_date}
                点赞人数： {likes}
                评论人数: {sprite_comment}
            '''
            print(goods_content)
    except NoSuchElementException as e:
        print(e)
def get_good(driver):
    # 通过JS控制滚轮滑动获取所有商品信息
    js_code = '''
                                        window.scrollTo(0,5000);
                                    '''
    driver.execute_script(js_code)  # 执行js代码
    # 等待数据加载
    time.sleep(2)
    # 商品详情wrap
    goods_detail = driver;
    # 商品名称
    goods_name = goods_detail.find_element_by_class_name('sku-name').text.replace("\n", " ")
    # 商品价格
    goods_price = goods_detail.find_element_by_class_name('price').text.replace("\n", " ")

    # 评价信息
    evaluation_btn = goods_detail.find_element_by_id('detail').find_element_by_class_name('tab-main').find_elements_by_tag_name('li')[4]
    evaluation_btn.click()
    print(evaluation_btn.text)
    time.sleep(2)
    # 好评度
    percent_con = goods_detail.find_element_by_class_name('percent-con').text.replace("\n", " ")
    # 评价tag
    evaluation_tags = goods_detail.find_elements_by_class_name('tag-1')
    tags = []
    for tag in evaluation_tags:
        tags.append(tag.text)
    # 评价类型
    evaluation_type_list = goods_detail.find_element_by_class_name('filter-list').find_elements_by_tag_name('li')
    types = []
    for type in evaluation_type_list:
        if (type.get_attribute('data-tab') == 'trigger'):
            types.append(type.find_element_by_tag_name('a').text)
    goods_content = f'''
                           商品名称: {goods_name}
                           商品价格: {goods_price}
                             好评度: {percent_con}
                           评价标签: {tags}
                           评价类型: {types}
                           \n
                          '''
    print(goods_content)

    ## 爬取评价信息
    get_evaluation(goods_detail)
    n =1
    # 爬取后面的页面
    while True:
        flag = isElementPresent(goods_detail, 'ui-pager-next')
        if flag:
            element = driver.find_element_by_class_name('ui-pager-next')
            driver.execute_script("arguments[0].click();", element)
            # 等待数据加载
            time.sleep(2)
            n = n+1
            ## 爬取评价信息
            get_evaluation(goods_detail)
            print('%d商品页数：' % n)
        else:
            print('到底了.')
            return
    print('商品总页数：%d' % n)
if __name__ == '__main__':

    # chrome_options = Options()
    # chrome_options.add_argument('--headless')
    # chrome_options.add_argument('--disable-gpu')
    # driver = webdriver.Chrome(options=chrome_options)

    # 获取用户商品的url
    urlList = input('请输入爬取商品url(以逗号分割):').strip()
    urlList = urlList.split(',')

    # 可视化界面  需要下载 chromeDiiriver 及 chrome浏览器
    driver = webdriver.Chrome()
    driver.implicitly_wait(5)

    for url in urlList:
        driver.get(url)
        get_good(driver)
    driver.close();





