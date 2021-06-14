import requests
from bs4 import BeautifulSoup
import re
from urllib.request import urlretrieve   #模組的檔案 request , class(工廠)方便使用資料型態 > 
import ssl 
ssl._create_default_https_context = ssl._create_unverified_context   #(備註：加了之後mac資料才跑出來）
import os

def download_images(articles):
    for article in articles:
        print(article.text,article['href'])
        if not os.path.isdir(os.path.join('download',article.text)):  ## General os.path.join ,  windows \ , Linux / 
            os.mkdir(os.path.join('download',article.text))
        res = requests.get('https://www.ptt.cc'+article['href'], headers={ 
        #request.get請求也要加上cookie，不然一樣會被18禁的cookie擋住
        "cookie":"over18=1"
    })  # 那篇文章所有HTML
        images = reg_imgur_file.findall(res.text)
        print(images)
        for image in set(images):   ## set 不會有重複的元素 >> list >> for loop
            ID = re.search('http[s]?://[i.]*imgur.com/(\w+\.(?:jpg|png|gif))',image).group(1)  #\w+\.(? 亂碼
            print(ID)
            urlretrieve(image, os.path.join('download',article.text,ID))   # (url, filename)  把'download',article.text, ID 接起來  #幾個參數就都接起來

def crawler():
    if not os.path.isdir('download'):
        os.mkdir('download')
    url = "https://www.ptt.cc/bbs/Beauty/index.html"    
    for round in range(3):
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
        download_images(articles)
        
reg_imgur_file  = re.compile('http[s]?://[i.]*imgur.com/\w+\.(?:jpg|png|gif)')
crawler()