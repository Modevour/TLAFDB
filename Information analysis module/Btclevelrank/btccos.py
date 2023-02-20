from lxml import etree
import requests


with open('btcdata.txt','r',encoding='utf-8') as f:
    data = f.readlines()
for lines in data:
    url = 'https://www.blockchain.com/btc/address/'
    requesturl = url + lines.strip()
    try:
        content =requests.get(requesturl).text
        # soup = bs4.BeautifulSoup(content,'html.parser')
        html = etree.HTML(content)  # 将网页源码转换为 XPath 可以解析的格式
        element = html.xpath('//*[@id = "__next"]/div[3]/div[2]/div/div/div[2]/div/div[1]/div[2]/div/div[4]/div[2]/span/text()')
        for line in element:
            with open('btcprpoint.txt','a+',encoding='utf-8') as f:
                f.write(lines.strip() + ' ' + line + '\n')
    except:
        print(lines+'出错了')
        continue