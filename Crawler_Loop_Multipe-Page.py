import requests
from bs4 import BeautifulSoup
import re

# url = 'https://www.ptt.cc/bbs/Grad-ProbAsk/index.html'
url = "https://www.ptt.cc/bbs/Beauty/index.html"

reg_imgur_file  = re.compile('http[s]?://[i.]*imgur.com/\w+\.(?:jpg|png|gif)')

for round in range(2):
    res = requests.get(url, headers={
        "cookie":"over18=1"
    })
    ##把抓到的res 告訴 BeautifulSoup 是html
    soup = BeautifulSoup(res.text,'html.parser')   ## "lxml == html.parser"
    ##抓取所有文章連結
    articles = soup.select('div.title a')
    # print(articles)
    ##選擇: [最舊, 上頁, 下頁, 最新
    paging = soup.select('div.btn-group-paging a')
    ##做成下頁的連結網址
    next_url = 'https://www.ptt.cc'+paging[1]['href'] 
    ##不然會抓到First Page
    url = next_url    
    ##text兩個[]文字,文章超連結
    for article in articles:
        print(article.text,article['href'])
        res = requests.get('https://www.ptt.cc'+article['href'], headers={ 
        #request.get請求也要加上cookie，不然一樣會被18禁的cookie擋住
        "cookie":"over18=1"
    })  # 那篇文章所有HTML
        images = reg_imgur_file.findall(res.text)
        print(images)
    