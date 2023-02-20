import re
import os
import requests
import time

def exact_vaildtransactionbtc():
    file_path = 'E:\\Dataexact\\allhtml'
    file_names = os.listdir(file_path)
    for i in range(1,len(file_names)):
    # print(os.path.join(file_path,file_names[i]))
        with open(os.path.join(file_path,file_names[i]), 'r', encoding='utf-8') as f:
             try:
                data = f.read()
             except:
                 continue
             else:
                addlist = []
                list1 =[]
                validaddress =[]
                addr1 = re.findall(r"bc1[a-zA-HJ-NP-Z0-9]{25,39}", data)
                for addrs1 in addr1:
                    if len(addrs1) == 42:
                        addlist.append(addrs1)
                        addlist = list(set(addlist))
                addr2 = re.findall(r"[13][a-km-zA-HJ-NP-Z1-9]{25,34}", data)
                for addrs2 in addr2:
                    if len(addrs2) == 34:
                        addlist.append(addrs2)
                        addlist = list(set(addlist)) # 筛选出的符合正则的地址列表
                for validbtc in addlist:
                    url = 'https://www.blockchain.com/search?search='
                    requesturl = url + validbtc
                    content = requests.get(requesturl).text
                    if len(re.findall('Oops! We couldn’t find what you are looking for.', content)) == 2:
                        list1.append(lines)
                for lines in addlist:
                    if lines not in list1:
                        validaddress.append(lines)  # 筛选出的有效地址列表
                for lines in validaddress:
                    # print(lines.strip())
                    url = 'https://www.blockchain.com/btc/address/'
                    requesturl = url + lines.strip()
                    # print(requesturl)
                    try:
                        content = requests.get(requesturl).text
                        time.sleep(1)
                    except:
                        with open('0000connecterror.txt', 'a+', encoding='utf-8') as f:
                            f.write(lines.strip() + '\n')
                            continue
                    else:
                        #筛选出存在真实交易的比特币地址
                        if len(re.findall('This address has transacted 0 times on the Bitcoin blockchain.',
                                          content)) == 1:
                            # if len(re.findall('This address has transacted 0 times on the Bitcoin blockchain. It has received a total of 0.00000000 BTC ($0.00) and has sent a total of 0.00000000 BTC ($0.00). The current value of this address is 0.00000000 BTC ($0.00).',content)) == 2:
                            with open('notransactionaddress.txt', 'a+', encoding='utf-8') as f:
                                f.write(lines.strip() + '\n')
                            # print(requesturl)
                        else:
                            with open('vaildtransactionaddress.txt', 'a+', encoding='utf-8') as f:
                                f.write(lines.strip() + '\n')
                            print('success')

if __name__ == '__main__':
      exact_vaildtransactionbtc()





