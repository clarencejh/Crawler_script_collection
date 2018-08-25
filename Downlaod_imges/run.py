# -*- coding: utf-8 -*-
"""
 多线程 异步下载 'http://www.doutula.com/photo/list/' 的表情包
"""


import re
import os
import requests
from lxml import etree
from urllib import request
import threading
from queue import Queue


class Produce_image_url(threading.Thread):
    def __init__(self, page_queue, img_url_queue, *args, **kwargs):
        super(Produce_image_url, self).__init__(*args, **kwargs)
        self.page_queue = page_queue
        self.img_url_queue = img_url_queue

    def run(self):
        while True:
            if self.page_queue.empty():
                print('"page_queue 队列为空 退出"')
                break
            page_url = self.page_queue.get()
            self.parse_page(page_url)

    def parse_page(self, url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
        }
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                text = response.text
            else:
                text = None
        except Exception:
            text = None

        if text:
            html = etree.HTML(text)
            img_list = html.xpath('//div[@class="page-content text-center"]//img[@class!="gif"]')
            for img in img_list:
                img_url = img.get('data-original')
                alt = img.get('alt')
                alt = re.sub(r'[\?\.!，\*]', '', alt)
                suffix = os.path.splitext(img_url)[1]
                filename = alt + suffix
                # 将获取到的img_url put到队列
                print(f'put {img_url} ===== {filename}')
                self.img_url_queue.put((img_url, filename))


class Download_image(threading.Thread):
    def __init__(self, page_queue, img_url_queue, *args, **kwargs):
        super(Download_image, self).__init__(*args, **kwargs)
        self.page_queue = page_queue
        self.img_url_queue = img_url_queue

    def run(self):
        print('Download_image start')
        while True:
            if self.page_queue.empty() and self.img_url_queue.empty():
                print('两个队列都为空, 退出')
                break
            img_url, filename = self.img_url_queue.get()
            th_name = threading.current_thread()
            print(f"{th_name}开始异步下载: ", filename)
            request.urlretrieve(img_url, 'images/' + filename)
            print(f'{th_name}已缓存图片 -> ', filename)


def main():
    page_queue = Queue(100)
    img_url_queue = Queue(1000)
    for i in range(1, 100):
        url = f'http://www.doutula.com/photo/list/?page={i}'
        page_queue.put(url)

    # 开启五个 获取 img_url的线程
    for i in range(5):
        p = Produce_image_url(page_queue=page_queue, img_url_queue=img_url_queue)
        p.start()

    # 开启五个下载图片的线程
    for i in range(5):
        d = Download_image(page_queue=page_queue, img_url_queue=img_url_queue)
        d.start()


if __name__ == '__main__':
    main()
