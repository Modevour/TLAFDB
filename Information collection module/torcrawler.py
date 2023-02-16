import requests
import re
from requests_html import HTMLSession

#方法二，由于暗网页面的变换性，因此在保存暗网爬取页面的同时收集出现在页面中v3洋葱域名
def gethtml():
    session = HTMLSession()
    proxy = {"http": "socks5h://127.0.0.1:9150","https": "socks5h://127.0.0.1:9150"}
    with open('onion.txt', 'r', encoding='utf-8') as fd:
        lines = fd.readlines()
        for line in lines:
            userfulurl = "http://"+line.rstrip()
            try:
                req = session.get(userfulurl, proxies=proxy)
            except (requests.exceptions.ConnectionError,requests.exceptions.ChunkedEncodingError):
                print (userfulurl+"连接出错了")
                with open('error.txt','a',encoding='utf-8') as file:
                    file.write('\n'+userfulurl)
            else:
                v3onion = re.findall(r"[0-9a-zA_Z]{56}\.onion", str(req.content))
                for lines in v3onion:
                    if len(lines) == 62:
                        with open(r"v3onion.txt", "a+") as f:
                            f.write(lines + "\n")
                with open(line.rstrip()+ ".html", "wb") as f:
            # 写文件用bytes而不是str，所以要转码   
                    f.write(req.content)

if __name__ == '__main__':
    gethtml()