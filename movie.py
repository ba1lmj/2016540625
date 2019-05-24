#导入所需库
import requests
from bs4 import BeautifulSoup
import wordcloud
import jieba
import time
#电影id
movie_id =24773958

#获取单页的评论，返回评论列表
def onepage(url):
    r = requests.get(url)
    r.encoding = "utf-8"
    html = r.text
    soup = BeautifulSoup(html,"html.parser")
    comments_sec = soup.find("div","mod-bd")
    comments_list =comments_sec.find_all("p", "")
    lst = []
    for i in range(len(comments_list)):
        lst.append(comments_list[i].text.strip())
     return lst

#获取多页评论，返回总列表
def parsepage(movie_id, page_num):
    data = []
    for i in range(page_num):
        url ="https://movie.douban.com/subject/" + str(movie_id) +"/comments?start=" + str(20 * i) + "&limit=20"
        data += onepage(url)
        print("parsing page %d" %(i+1))
        time.sleep(6)#每隔6秒爬取一页，豆瓣默认5秒，太频繁了不好哦
     return "".join(data)


def main():
    data = parsepage(movie_id, 10)#10为要爬取的页数
    all_comments = jieba.lcut(data)
    words = " ".join(all_comments)
    print("正在生成词云图……")
    wc=wordcloud.WordCloud(width=1500,height=1500,background_color="white",font_path="./msyh.ttc")
    wc.generate(words)
    wc.to_file("c://admin//Desktop//image.jpg")
    print("ok")


main()
print('image.jpg')