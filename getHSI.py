import requests
import html5lib

proxies = {
    "http": "http://127.0.0.1:1080",
    "https": "http://127.0.0.1:1080",
}

s=requests.Session()
p = html5lib.HTMLParser(html5lib.treebuilders.getTreeBuilder("lxml"))
res=s.get("https://www.gswarrants.com.hk/cgi/tools/hsi.cgi?sort=0&sort1=0",proxies=proxies)
soup = p.parse(res.text)
print(soup.findAll("table",{"class":"tb_b"}))