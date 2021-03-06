# -*- coding: utf-8 -*-

import re
import time
from datetime import datetime
# import requests
from newspaper import Article


def parse_publish_time(html_str):
    """
    正则匹配出 html_str 中的 日期时间（日期与时间之间的间隔小于20个字符）
    返回 日期时间 2019-04-13 14:08:15
    返回 日期时间的时间戳 1555135695
    :param html_str:
    :return:
    """
    regex_str_list = [
        {'name': 'all', 'regex_str': r'(\d{4})[ 年/\.-](\d{1,2})[ 月/\.-](\d{1,2})[ 日].{0,20}?(\d{1,2})[:：](\d{1,2})[:：](\d{1,2})'},  # 2019/1/1 11:11:11
        {'name': 'whitout_S', 'regex_str': r'(\d{4})[ 年/\.-](\d{1,2})[ 月/\.-](\d{1,2})[ 日].{0,20}?(\d{1,2})[:：](\d{1,2})'},  # 2019/1/1 11:11
        {'name': 'whitout_Y', 'regex_str': r'(\d{4})[ 年/\.-](\d{1,2})[ 月/\.-](\d{1,2})[ 日].{0,20}?(\d{1,2})[:：](\d{1,2})[:：](\d{1,2})'},  # 1/1 11:11:11
        {'name': 'whitout_Y_S', 'regex_str':  r'(\d{1,2})[ 月/\.-](\d{1,2})[ 日].{0,20}?(\d{1,2})[:：](\d{1,2})'},  # 1/1 11:11
        {'name': 'whitout_H_m_S', 'regex_str': r'(\d{4})[ 年/\.-](\d{1,2})[ 月/\.-](\d{1,2})[ 日]'},  # 2020年2月27日
    ]

    now_time = datetime.now()
    now_time_str = now_time.strftime('%Y-%m-%d %H:%M:%S')

    publish_time = ''

    for temp in regex_str_list:
        regex_name = temp['name']
        regex_str = temp['regex_str']
        try:
            re_result = re.findall(regex_str, html_str)
            if re_result:
                for items in re_result:
                    items = list(items)

                    if regex_name == 'whitout_S':
                        items.append('00')  # 没有发布时间的秒时，填入秒的默认值 00
                    if regex_name == 'whitout_Y':
                        items.insert(0, str(now_time.year))  # 没有发布时间的年时，填入年的默认值 当前时间的年
                    if regex_name == 'whitout_Y_S':
                        items.insert(0, str(now_time.year))  # 没有发布时间的年时，填入年的默认值 当前时间的年
                        items.append('00')  # 没有发布时间的秒时，填入秒的默认值 00
                    if regex_name == 'whitout_H_m_S':
                        items.append('00')
                        items.append('00')
                        items.append('00')

                    # 处理 publish_time 的格式
                    def add_0(num_str):  # 在只有一位数的值前面补个0
                        if len(num_str) == 1:
                            return '0' + num_str
                        else:
                            return num_str

                    items = list(map(add_0, items))

                    # 验证日期时间是否正确
                    # 验证 日期 时间 的数值
                    if 0 <= int(items[0]) and 1 <= int(items[1]) <= 12 and 1 <= int(items[2]) <= 31 and 0 <= int(items[3]) <= 24 and 0 <= int(items[4]) <= 59 and 0 <= int(items[5]) <= 59:
                        publish_time = '{}-{}-{} {}:{}:{}'.format(items[0], items[1], items[2], items[3], items[4], items[5])
                    else:
                        publish_time = ''
                        print('[try match publish_time] match failed, use', '"' + regex_name + '"')
                        continue
                    # 验证 时间长度正确 且 发布时间不晚于当前时间
                    if 14 < len(publish_time) < 20 and publish_time <= now_time_str:
                        break
                    else:
                        publish_time = ''
                        print('[try match publish_time] match failed, use', '"' + regex_name + '"')
                        continue
            else:
                print('[try match publish_time] match failed, use', '"' + regex_name + '"')
                # pass

            if publish_time:
                break
        except Exception as e:
            # print('[Error] wrong datetime format')
            print('[error][parse_publish_time][', datetime.now(), '][msg:', str(e), ']')
            publish_time = ''

    if not publish_time:
        # print('use now_time as default publish_time')
        # publish_time = now_time_str
        print("use '' as default publish_time")
        publish_time = ''
        publish_timestamp = ''

        print(publish_time, publish_timestamp)
        return publish_time, publish_timestamp

    if publish_time >= '1970-01-01 08:00:00':
        publish_timestamp = int(time.mktime(time.strptime(publish_time, '%Y-%m-%d %H:%M:%S')))
    else:
        publish_timestamp = -1
        
    print(publish_time, publish_timestamp)
    return publish_time, publish_timestamp


if __name__ == '__main__':
    # headers = {
    #     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36"
    # }

    # '2019年1月1日'
    # '2019年01月01日'
    # '2019/1/1'
    # '2019/01/01'
    # '2019.1.1'
    # '2019.01.01'
    # '2019-1-1'
    # '2019-01-01'
    # 
    # '    <span class="source ent-source">2019年3月4日，比赛得分1：0</span></div>'
    # html_str = """<div class="second-title">都说险资这轮“上车”早 看看他们潜伏哪些票？</div>
    # <div class="date-source" data-sudaclick="content_media_p">
    #         <span class="date">2019-04-12 8:32:54</span>
    #     <span class="source ent-source">中国证券网</span></div>
    #     """

    url = 'http://stock.hexun.com/2019-04-13/196813433.html'
    news = Article(url, language='zh')
    news.download()
    html_str = news.html

    publish_time, publish_timestamp = parse_publish_time(html_str)
    print('==========main============')
    print(publish_time, publish_timestamp)
    print(url)
