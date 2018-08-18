"""
爬取taptap两个排行榜的游戏,获取评论, 存入数据库
create time: 2018.6.28
"""

import time
import requests
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
from pymongo import MongoClient

# 连接数据库
db = MongoClient()
# 创建表

# 游戏信息表
game_info = db.taptap_db.game_info
# 评论表
comment_db = db.taptap_db.comment_db

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36"
}


def get_html_text(url):
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None


def parpse_htmltext(key, html):
    soup = BeautifulSoup(html, "lxml")
    try:
        id_list = [soup.select(".card-middle-title")[i]["href"].split("/")[-1] for i in range(30)]

        title_list = soup.select(".card-middle-title > h4")
        score_list = soup.select(".middle-footer-rating > span")
        game_tpye_list = soup.select(".card-middle-footer > a")
        publisher_list = soup.select(".card-middle-author > a")
        datas = list()
        for id, title, score, game_type, pulibsher in zip(id_list, title_list, score_list, game_tpye_list, publisher_list):
            data = {
                "id": id,                                   # 游戏id
                "title": title.get_text().strip(),          # 游戏名
                "score": score.get_text().strip(),          # 游戏评分
                "game_type": game_type.get_text().strip(),  # 游戏类型
                "pulisher": pulibsher.get_text().strip(),   # 厂商
                "from": key                                 # 从哪个排行榜来
            }
            datas.append(data)  
    except Exception as e:
        print(e)
    # 返回字典列表
    finally:
        return datas


# 获取游戏下面的评论
def get_game_commet(game_id):
    comment_url = "https://www.taptap.com/app/{}/review".format(game_id)
    response = get_html_text(comment_url)
    soup = BeautifulSoup(response, "lxml")

    # 用户名
    names = soup.select(".taptap-review-item.collapse.in > div > div.item-text-header > span > a")
    # 评论内容
    comments = soup.select(".taptap-review-item.collapse.in > div > div.item-text-body")
    # 获得的点赞数
    receive_praises = soup.select(
        ".taptap-review-item.collapse.in > div > div.item-text-footer > ul > li > [data-value=up] > span")
    comments_list = list()
    for name, comment, receive_praise in zip(names, comments, receive_praises):
        data = {
            "game_id": game_id,                             # 游戏id
            "username": name.get_text(),                    # 评论用户名
            "comment": comment.get_text(),                  # 评论内容
            "receive_praise": receive_praise.get_text()     # 获得的点赞数     可以加一些其他的..
        }
        comments_list.append(data)
    return comments_list


# 储存到数据库
def output(db, data):
    # 去重操作
    id_list = db.update({'game_id': data['game_id']}, {'$set': data}, True)
    # id_list = db.insert_many(data)
    # return id_list
    return id_list


# 主函数
def main():
    urls = {
        "Android": "https://www.taptap.com/top/download",
        "iOS": "https://www.taptap.com/top/ios",
    }
    for key, value in urls.items():
        html = get_html_text(value)
        data_list = parpse_htmltext(key, html)
        # 将游戏储存到数据库
        output(game_info, data_list)

        print([data_list[i]['title'] for i in range(len(data_list))])
        # 获取评论
        for data in data_list:
            game_id = data["id"]
            comment_list = get_game_commet(game_id)
            output(comment_db, comment_list)
            print(" '{}' 评论获取成功".format(data['title']))
            time.sleep(0.5)


if __name__ == '__main__':
    main()
