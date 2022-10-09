# 下载2022年阳光学业评价五年级语文上册人教版参考答案
import requests
import random
import os
from bs4 import BeautifulSoup

def main():

    for i in list_img_src():
        download(i)

def download(url):
    # url = 'http://thumb.1010pic.com/pic19/519236/new/a60b07edbe3d178413c9c244b8d48146.jpg'
    p = './download/'
    if not os.path.exists(p):
        os.makedirs(p)
    fname = p + url.split('/')[-1]

    try:
        headers = get_headers()
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        # print(r.status_code)
        open(fname, 'wb').write(r.content)
    except:
        print('Failed to download file')


def list_img_src():
    url = 'http://www.1010jiajiao.com/daan/chapter_34430657.html'
    headers = get_headers()
    lst = []
    # for x in range(30657, 30666): #五年级语文上册
    # for x in range(30345, 30359): #五年级英语上册
    # for x in range(29800, 29809): #五年级数学上册
    all = list(range(30657, 30666)) + list(range(30345, 30359)) + list(range(29800, 29809))
    for x in all: # All
        url = 'http://www.1010jiajiao.com/daan/chapter_344' + str(x) + '.html'
        img = img_src(url, headers)
        print(img)
        lst.append(img)

    return lst

def img_src(url, headers):
    try:
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        # print(r.status_code)
        r.encoding = r.apparent_encoding
        # print(r.text)
        soup = BeautifulSoup(r.text, 'html.parser')
        # print(soup.prettify())
    except:
        print('Failed to get image src from ' + url)
    else:
        div = soup.find(id="img1")
        # print(div)
        # print(div.img)
        # print(div.img['src'])
        return div.img['src']

def get_headers():
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0",
        "Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0",
        "Mozilla/5.0 (X11; Linux x86_64; rv:95.0) Gecko/20100101 Firefox/95.0"
    ]
    random_user_agent = random.choice(user_agents)
    headers = {
        'User-Agent': random_user_agent
    }

    return headers

if __name__ == "__main__":
    main()

