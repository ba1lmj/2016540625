#第一步要对网页进行访问
from urllib import request
from bs4 import BeautifulSoup as bs
import re
import jieba  # 分词包
import pandas as pd
import numpy
import matplotlib
matplotlib.rcParams['figure.figsize'] = (10.0, 5.0)
from matplotlib import pyplot as plt
from wordcloud import WordCloud
from scipy.misc import imread
resp = request.urlopen('https://movie.douban.com/cinema/nowplaying/changsha/')
html_data = resp.read().decode('utf-8')
print(html_data)

soup = bs(html_data, 'html.parser')

nowplaying_movie = soup.find_all('div', id="nowplaying")
nowplaying_movie_list = nowplaying_movie[0].find_all('li',class_='list-item')

nowplaying_list = []
for item in nowplaying_movie_list:
        nowplaying_dict = {}
        nowplaying_dict['id'] = item['data-subject']
        for tag_img_item in item.find_all('img'):
            nowplaying_dict['name'] = tag_img_item['alt']
            nowplaying_list.append(nowplaying_dict)
            print(nowplaying_dict['name'])
print(nowplaying_list[3]['id'])

for movie in range(5):
    requrl = 'https://movie.douban.com/subject/' + nowplaying_list[movie]['id'] + '/comments' +'?' +'start=0' + '&limit=1000'
    resp = request.urlopen(requrl)
    html_data = resp.read().decode('utf-8')
    soup = bs(html_data, 'html.parser')
    comment_div_lits = soup.find_all('span', class_='short')
    print(comment_div_lits)

for item in comment_div_lits:
    if item.find_all('span')[0].string is not None:
        eachCommentList.append(item.find_all('span')[0].string)
    print(eachCommentList)
comments = ''
for k in range(len(comment_div_lits)):
    comments = comments + (str(comment_div_lits[k])).strip()
print(comments)

pattern = re.compile(r'[\u4e00-\u9fa5]+')
filterdata = re.findall(pattern, comments)
cleaned_comments = ''.join(filterdata)
print(cleaned_comments)

segment = jieba.lcut(cleaned_comments)
words_df = pd.DataFrame({'segment': segment})
print(words_df)

stopwords = pd.read_csv("D:\PyCharm2018.3.1\chineseStopWords.txt", index_col=False, quoting=3, sep="\t", names=['stopword'], encoding='utf-8')  # quoting=3全不引用
words_df = words_df[~words_df.segment.isin(stopwords.stopword)]
print(words_df.head())

words_stat = words_df.groupby(by=['segment'])['segment'].agg({"计数": numpy.size})
words_stat = words_stat.reset_index().sort_values(by=["计数"], ascending=False)
print(words_stat.head())


matplotlib.rcParams['figure.figsize'] = (10.0, 5.0)
wordcloud = WordCloud(font_path="simhei.ttf",background_color="white",max_font_size=80)
word_frequence = {x[0]:x[1] for x in words_stat.head(1000).values}
wordcloud=wordcloud.fit_words(word_frequence)
plt.imshow(wordcloud)
plt.show()