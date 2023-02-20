import re
import csv

Onionv3list = []
bitcoinlist = []
finabitcoinlist = []
list1 = []
infolist ={}
header = ['btc','Onion v3隐藏服务地址','数量']

with open(r"validtransactionbtcinfo.csv", 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    for row in reader:
        infolist[row['name']] = row['bitcoin']
# print(infolist)
with open(r'vaildtransactionaddress.txt','r',encoding='utf-8') as f:
            data = f.readlines()
csvfile = open(r'result.csv', 'a+', encoding='utf-8-sig', newline='')
writeobj = csv.DictWriter(csvfile, fieldnames=header)
writeobj.writeheader()

for lines in data:
    finainfolist = {}
    list2 = []
    finainfolist['btc'] =lines.strip()
    for k,v in infolist.items():
        #bc1正则表达式：bc1[a-zA-HJ-NP-Z0-9]{25,39}
        #13正则表达式：[13][a-km-zA-HJ-NP-Z1-9]{25,34}
        #print(v)
        for line in v.replace("['",'').replace("']",'').split("', '"):
            #print(line)
            #if re.findall(lines.strip(),str(re.match('([13]|bc1)[a-zA-HJ-NP-Z0-9]{25,39}',line.strip())).replace("['",'').replace("']",'')):
            if re.findall(lines.strip(),re.match('([13]|bc1)[a-zA-HJ-NP-Z0-9]{25,39}', line).group()):
                #print(k.strip())
                list2.append(k.strip())
    finainfolist['Onion v3隐藏服务地址'] = list(set(list2))
    finainfolist['数量'] = len(list(set(list2)))
    csvfile = open(r'result.csv', 'a+', encoding='utf-8-sig', newline='')
    writeobj = csv.DictWriter(csvfile, fieldnames=header)
    writeobj.writerow(finainfolist)


