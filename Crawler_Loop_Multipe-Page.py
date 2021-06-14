import requests
from bs4 import BeautifulSoup

url = 'https://www.ptt.cc/bbs/Beauty/index.html'
       
for round in range(2):
    res = requests.get(url, headers={
        "cookie":"over18=1"
    })
    ##把抓到的res 告訴 BeautifulSoup 是html
    soup = BeautifulSoup(res.text,'html.parser')   ## "lxml == html.parser"
    ##抓取所有文章連結
    articles = soup.select('div.title a')
    ##選擇: [最舊, 上頁, 下頁, 最新
    paging = soup.select('div.btn-group-paging a')
    ##做成下頁的連結網址
    next_url = 'https://www.ptt.cc'+paging[1]['href'] 
    ##不然會抓到First Page
    url = next_url    
    ##text兩個[]文字,文章超連結
    for article in articles:
        print(article.text,article['href'])


