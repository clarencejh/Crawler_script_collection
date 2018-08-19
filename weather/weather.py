# -*- coding: utf-8 -*-
import requests
import time
from bs4 import BeautifulSoup
from requests.exceptions import RequestException
from pymongo import MongoClient

db = MongoClient()
weather = db.weather.citys


def get_page_text(url):
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code:
            # 编码有问题
            return response.content.decode('utf-8')
        return None
    except RequestException as e:
        print(e)
        return None


def item(data_list):
    data = {
        'city': data_list[-10],                          # 城市
        'day_weather': ' '.join(data_list[-9:-6]),      # 白天天气
        'max_temperature':data_list[-6],                 # 最高气温
        'night_weather': ' '.join(data_list[-5:-2]),     # 晚上天气
        'min_temperature': data_list[-2]                 # 最低气温
    }
    return data


# 解析页面  提取各个城市的天气信息, 并返回 如上 格式的item
def parse_page(text):
    soup = BeautifulSoup(text, 'lxml')
    table = soup.select('table')[0]
    # for table in tables:
    trs = table.select('tr')[2:]
    for tr in trs:
        data_list = list(tr.stripped_strings)
        data = item(data_list)
        yield data


# 获取所有区域的url
def find_all_url(text):
    baes_url = 'http://www.weather.com.cn'
    soup = BeautifulSoup(text, 'lxml')
    a_list = soup.select('.lq_contentboxTab2 a')
    href_list = [baes_url+a.get('href') for a in a_list]
    return href_list


# 存储到 MongoDB
def output(data):
    tianqi.insert_one(data)


def main():
    url = 'http://www.weather.com.cn/textFC/hb.shtml'
    html = get_page_text(url)
    url_list = find_all_url(html)
    for url in url_list:
        html = get_page_text(url)
        for data in parse_page(html):
            output(data)
            print('储存成功 ', data)
        time.sleep(2)


if __name__ == '__main__':
    main()
