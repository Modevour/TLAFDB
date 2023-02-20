import csv
import re
header = ['btc', 'rank', 'amount', 'classify', 'name', 'pagerank']
Sdanger = ['market', 'hacking', 'drugs', 'porn', 'gun', 'kill', 'gamble']
Adanger = ['forum', 'blog', 'btc', 'news', 'card', 'transaction']
Bdanger = ['other', 'door']
list_SSS = []
list_SS1 = []
list_SS = []
list_SS2 = []
list_S = []
list_A = []
list_B = []
with open(r'btcprpoint.txt', 'r', encoding='utf-8') as file:
    btcprpoint_data = file.readlines()
with open(r'processrespagerank.txt', 'r', encoding='utf-8') as file:
    pagerank_data = file.readlines()
with open(r'1same.txt', 'r', encoding='utf-8') as file:
    nointersaction_list = file.readlines()
with open(r'2same.txt', 'r', encoding='utf-8') as file:
    twointersaction_list = file.readlines()
with open(r'3same.txt', 'r', encoding='utf-8') as file:
    threeintersaction_list = file.readlines()
for unit in threeintersaction_list:
    info_dic = {'btc': unit.split(':')[0],
                'classify': unit.split(':')[1].replace('\n', ''),
                'rank': 'SSS',
                'name': ''}
    name_list = []
    for line in btcprpoint_data:
        if info_dic['btc'] == line.split(' ')[0]:
            amount = line.split(' ')[1]
            info_dic['amount'] = float(amount)
    with open(r'validtransactionbtcinfo.csv', 'r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if len(re.findall(info_dic['btc'], row['bitcoin'])) != 0:
                name_list.append(row['name'])
    com_dic = {}
    rankname = []
    for name in name_list:
        for lines in pagerank_data:
            if name == lines.split(' ')[0]:
                com_dic[name] = float(lines.split(' ')[1])
                rankname.append(name)
    for name in name_list:
        if name not in rankname:
            com_dic[name] = 0
    rank = sorted(com_dic.items(), key=lambda item: item[1], reverse=True)
    top_name = rank[0]
    info_dic['name'] = top_name[0]
    info_dic['pagerank'] = top_name[1]
    list_SSS.append(info_dic)
for unit in twointersaction_list:
    info_dic = {'btc': unit.split(':')[0],
                'classify': unit.split(':')[1].replace('\n', ''),
                'rank': 'SS',
                'name': ''}
    name_list = []
    for line in btcprpoint_data:
        if info_dic['btc'] == line.split(' ')[0]:
            amount = line.split(' ')[1]
            info_dic['amount'] = float(amount)
    with open(r'validtransactionbtcinfo.csv', 'r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if len(re.findall(info_dic['btc'], row['bitcoin'])) != 0:
                name_list.append(row['name'])
    com_dic = {}
    rankname = []
    for name in name_list:
        for lines in pagerank_data:
            if name == lines.split(' ')[0]:
                com_dic[name] = float(lines.split(' ')[1])
                rankname.append(name)
    for name in name_list:
        if name not in rankname:
            com_dic[name] = 0
    rank = sorted(com_dic.items(), key=lambda item: item[1], reverse=True)
    top_name = rank[0]
    info_dic['name'] = top_name[0]
    info_dic['pagerank'] = top_name[1]
    list_SS.append(info_dic)
for unit in nointersaction_list:
    info_dic = {'btc': unit.split(':')[0],
                'classify': unit.split(':')[1].replace('\n', ''),
                'name': ''}
    name_list = []
    for line in btcprpoint_data:
        if info_dic['btc'] == line.split(' ')[0]:
            amount = line.split(' ')[1]
            info_dic['amount'] = float(amount)
    with open(r'validtransactionbtcinfo.csv', 'r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if len(re.findall(info_dic['btc'], row['bitcoin'])) != 0:
                name_list.append(row['name'])
    com_dic = {}
    rankname = []
    for name in name_list:
        for lines in pagerank_data:
            if name == lines.split(' ')[0]:
                com_dic[name] = float(lines.split(' ')[1])
                rankname.append(name)
    for name in name_list:
        if name not in rankname:
            com_dic[name] = 0
    rank = sorted(com_dic.items(), key=lambda item: item[1], reverse=True)
    top_name = rank[0]
    info_dic['name'] = top_name[0]
    info_dic['pagerank'] = top_name[1]
    if info_dic['classify'].replace("['", '').replace("']", '') in Sdanger:
        info_dic['rank'] = 'S'
        list_S.append(info_dic)
    if info_dic['classify'].replace("['", '').replace("']", '') in Adanger:
        info_dic['rank'] = 'A'
        list_A.append(info_dic)
    if info_dic['classify'].replace("['", '').replace("']", '') in Bdanger:
        info_dic['rank'] = 'B'
        list_B.append(info_dic)
list_SSS = sorted(list_SSS, key=lambda dict: dict['amount'])
list_SSS.reverse()
list_SS = sorted(list_SS, key=lambda dict: dict['amount'])
list_SS.reverse()
list_S = sorted(list_S, key=lambda dict: dict['amount'])
list_S.reverse()
list_A = sorted(list_A, key=lambda dict: dict['amount'])
list_A.reverse()
list_B = sorted(list_B, key=lambda dict: dict['amount'])
list_B.reverse()
for units in list_SS:
    index_key = list_SS.index(units)
    classify_list = units['classify'].replace("'", '').replace("[", '').replace(']', '').split(', ')
    for unit in classify_list:
        if unit in Sdanger:
            list_SS1.append(units)
for units in list_SS:
    index_key = list_SS.index(units)
    classify_list = units['classify'].replace("'", '').replace("[", '').replace(']', '').split(', ')
    for unit in classify_list:
        if unit in Bdanger:
            list_SS2.append(units)
new_list_SS = []
for ss in list_SS:
    if ss not in list_SS1 and ss not in list_SS2:
        new_list_SS.append(ss)
list_SS1 = sorted(list_SS1, key=lambda dict: dict['amount'])
list_SS1.reverse()
list_SS2 = sorted(list_SS2, key=lambda dict: dict['amount'])
list_SS2.reverse()
new_list_SS = sorted(new_list_SS, key=lambda dict: dict['amount'])
new_list_SS.reverse()
csvfile1 = open(r'btclevelrank1.csv', 'a+', encoding='utf-8-sig', newline='')
writeobj = csv.DictWriter(csvfile1, fieldnames=header)
for info_dic in list_SSS:
    writeobj.writerow(info_dic)
for info_dic in list_SS1:
    writeobj.writerow(info_dic)
for info_dic in new_list_SS:
    writeobj.writerow(info_dic)
for info_dic in list_SS2:
    writeobj.writerow(info_dic)
for info_dic in list_S:
    writeobj.writerow(info_dic)
for info_dic in list_A:
    writeobj.writerow(info_dic)
for info_dic in list_B:
    writeobj.writerow(info_dic)