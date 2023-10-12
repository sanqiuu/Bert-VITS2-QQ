import requests
import json
from bs4 import BeautifulSoup

def katakana(content):
    url = 'https://www.chineseconverter.com/zh-cn/convert/chinese-characters-to-katakana-conversion'
    client = requests.session()
    rep=client.get(url)
    cookie=client.cookies
    headers=client.headers
    csrf=Find(rep.content)
    # csrf=cookie['_csrf-frontend']
    data={"ChineseToKatakana[type]": "pinyin","ChineseToKatakana[languageType]": "hiragana"}
    data["ChineseToKatakana[input]"]=content
    data['_csrf-frontend']=csrf
    # print(data)
    rep=client.post(url,headers=headers,cookies=cookie,data=data)
    html = rep.content.decode('utf-8')
    # print(html)
    bs=BeautifulSoup(html,'lxml')
    # print(html)
    tmp=bs.find_all('div',{'class':"thumbnail result-html"})
    return tmp[0].contents[0].strip("\n").strip()

def Find(html):
    bs=BeautifulSoup(html,'lxml')
    # print(html)
    tmp=bs.find_all('input',{'name':"_csrf-frontend"})
    return tmp[0]['value']

def test():
    url = 'https://www.chineseconverter.com/zh-cn/convert/chinese-characters-to-katakana-conversion'
    client = requests.session()
    client.get(url)
    cookie=client.cookies
    print(cookie['_csrf-frontend'])
    print(cookie)