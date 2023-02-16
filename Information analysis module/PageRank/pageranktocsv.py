import csv
##将pagerank数据写入csv文件保存
header = ['url', 'prpoint']
with open('processrespagerank.txt', 'r', encoding='utf-8') as f:
    data = f.readlines()
onionrankurl =[]
onionrankpoint=[]
for points in data:
    url = points.split(' ')[0]
    propoint =points.split(' ')[1].replace('\n','')
    onionrankurl.append(url)
    onionrankpoint.append(propoint)

for i in range(0,len(onionrankpoint)):
    info_dict = {}
    info_dict['url'] = onionrankurl[i]
    info_dict['prpoint'] = onionrankpoint[i]
    csvfile = open('pagerankpoint.csv', 'a+', encoding='utf-8-sig', newline='')
    writeobj = csv.DictWriter(csvfile, fieldnames=header)
    writeobj.writerow(info_dict)