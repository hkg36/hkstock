import requests
from bs4 import BeautifulSoup

proxies = {
    "http": "http://127.0.0.1:1080",
    "https": "http://127.0.0.1:1080",
}

s=requests.Session()

res=s.get("https://www.gswarrants.com.hk/cgi/tools/hsi.cgi?sort=0&sort1=0",proxies=proxies)
soup = BeautifulSoup(res.text, 'html.parser')
print(soup.findAll("table",{"class":"tb_b"}))