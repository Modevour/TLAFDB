import re
import os
import csv
import bs4
import requests
import nltk
import time
from nltk.tokenize import sent_tokenize, word_tokenize
import nltk.data
from nltk.corpus import stopwords
import string
from nltk.text import TextCollection
from nltk.stem.lancaster import LancasterStemmer
from nltk.stem import WordNetLemmatizer
file_path = 'E:\\Dataexact\\allhtml'
file_names = os.listdir(file_path)
header = ['name', 'title', 'classify','bitcoin']


def get_keywords(pagetext):
    pagetext = str.lower(pagetext)
    pagetext = re.sub('[0-9]', ' ', pagetext)
    pagetext = re.sub('[@#$%&*()_=+|/?<>€;✔:♦{}.฿©]', ' ', pagetext)
    sent_tokenize_list = sent_tokenize(pagetext)
    alltokens = []
    for sent in sent_tokenize_list:
        for word in word_tokenize(sent):
            alltokens.append(word)
    cleanTokens = []
    for token in alltokens:
        if token not in stopwords.words('english') and token not in string.punctuation:
            cleanTokens.append(token)
    lancaster_stemmer = LancasterStemmer()
    wordnet_lemmatizer = WordNetLemmatizer()
    for token in cleanTokens:
        token = wordnet_lemmatizer.lemmatize(lancaster_stemmer.stem(token))
    posTagging = nltk.pos_tag(cleanTokens)
    cleanTokens = [m for m in cleanTokens if len(m) > 2]
    corpus = TextCollection(cleanTokens)
    words = set(cleanTokens)
    value = {}
    for word in words:
        value[word] = round(corpus.tf_idf(word, cleanTokens) * 100, 2)
    rank = sorted(value.items(), key=lambda item: item[1], reverse=True)
    return rank[0:8]


def classify(keylist):
    tag = ''
    keylist = re.sub('[0-9]', '', str(keylist)).replace("[('", '').replace("'", '').replace('), (', '').replace(', .)]', '').replace(
        '.', '')
    keymatch_list = []
    classify_list = [['market','empire','dream','member','products','seller','feedbackshow','vendor'],#市场类
                     ['hackers', 'hacked', 'backdoor', 'malware', 'hacker', 'threat', 'cracking',
                      'hacking', 'hack', 'hacks','backdoor','cracking'],#黑客类
                     ['cocaine', 'cannabis', 'lsd', 'meth', 'pills', 'drugs', 'drugstore', 'xanax', 'heroin',
                      'crystal', 'poison','poisons', 'drug', 'psychedelics'],#毒品类
                     ['porn', 'pussy', 'lolita', 'livejasmin', 'girls', 'porno', 'sex', 'bitch', 'incest', 'videos',
                      'love', 'teen'],#色情类
                     ['ammo', 'guns', 'rifles', 'firearms', 'poudriere', 'armory', 'arms', 'gun', ' pistol',
                      'cartridge','barrel'],#枪支类
                     ['hitman', 'killer', 'hitmen', 'red', 'killing', 'kill', 'blood', 'dead', 'assassination'],#谋杀类
                     ['football','cost','matches','rate','score','scams'],#赌博类
                     ['forum','insider','topics','information','post','tips'],#论坛类
                     ['blog'],#博客类
                     ['bitcoin','wallet','wallets','double','multiply','receive','price','blockchain','amount','10x','100x',
                      'Doubler','Officially'],#比特币投资类
                     ['bbc', 'news','company','moreapr'],#新闻类
                     ['card','cards', 'payment','buy','buyer','send','balance','minimum','maximum','counterfeits',
                        'paypal','passport'],#贩卡类
                     ['transfer','perfectmoney','cashout','coinchargebacks','escrow','apple','iphone',
                      'profit','skrill','usd','trading']]#交易类

    try:
        keymatch_list = keylist.split(', ')
        for key in keymatch_list:
            if key in classify_list[0]:
                tag = 'market'
                break
            if key in classify_list[1]:
                tag = 'hacking'
                break
            if key in classify_list[2]:
                tag = 'drugs'
                break
            if key in classify_list[3]:
                tag = 'porn'
                break
            elif key in classify_list[4]:
                tag = 'gun'
                break
            elif key in classify_list[5]:
                tag = 'kill'
                break
            elif key in classify_list[6]:
                tag = 'gamble'
                break
            elif key in classify_list[7]:
                tag = 'forum'
                break
            elif key in classify_list[8]:
                tag = 'blog'
                break
            elif key in classify_list[9]:
                tag = 'btc'
                break
            elif key in classify_list[10]:
                tag = 'news'
                break
            elif key in classify_list[11]:
                tag = 'card'
                break
            else:
                tag = 'transaction'
    except:
        tag = 'error'
    return tag


def get_info(filename):
    for i in range(0, len(filename)):
        info_dic = {}
        try:
            with open(os.path.join(file_path, filename[i]), 'r', encoding='utf-8') as f:
                filedata = f.read()
            soup = bs4.BeautifulSoup(filedata, features='lxml')
            title = soup.title.get_text()
            text = soup.get_text()
            keys = get_keywords(text)
            dooronions = re.findall('[0-9a-zA_Z]+\.onion', filedata)
            countlist = []
            addlist = []
            list1 = []
            validaddress = []
            finavalidaddress = []
            addr = re.findall(r"[13][a-km-zA-HJ-NP-Z1-9]{25,34}", filedata)
            for addrs in addr:
                if len(addrs) == 34:
                    addlist.append(addrs)
            addr2 = re.findall(r"bc1[a-zA-HJ-NP-Z0-9]{25,39}", filedata)
            for addrs2 in addr2:
                if len(addrs2) == 42:
                    addlist.append(addrs2)
            addlist = list(set(addlist))
            for lines in addlist:
                url = 'https://www.blockchain.com/search?search='
                requesturl = url + lines
                content = requests.get(requesturl).text
                if len(re.findall('Oops! We couldn’t find what you are looking for.', content)) == 2:
                    list1.append(lines)
            for lines in addlist:
                if lines not in list1:
                    validaddress.append(lines) #筛选出的有效地址列表
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
                    if len(re.findall('This address has transacted 0 times on the Bitcoin blockchain.', content)) == 1:
                        # if len(re.findall('This address has transacted 0 times on the Bitcoin blockchain. It has received a total of 0.00000000 BTC ($0.00) and has sent a total of 0.00000000 BTC ($0.00). The current value of this address is 0.00000000 BTC ($0.00).',content)) == 2:
                        with open('0000address.txt', 'a+', encoding='utf-8') as f:
                            f.write(lines.strip() + '\n')
                        # print(requesturl)
                    else:
                        with open('validaddress.txt', 'a+', encoding='utf-8') as f:
                            f.write(lines.strip() + '\n')
                        finavalidaddress.append(lines.strip())
                        print('success')
            for url in dooronions:
                countlist.append(url)
            countlist = list(set(countlist))
            if len(countlist) >= 20:
                if len(finavalidaddress) != 0:
                    info_dic['name'] = filename[i].replace('.html', '')
                    info_dic['title'] = title
                    info_dic['classify'] = 'door'
                    # info_dic['keys'] = re.sub('[0-9]', '', str(keys)).replace("[('", '').replace("'", '').replace('), (', '').replace(', .)]', '').replace('.', '')
                    info_dic['bitcoin'] = finavalidaddress
                    csvfile1 = open('validtransactionbtcinfo.csv', 'a+', encoding='utf-8-sig', newline='')
                    writeobj = csv.DictWriter(csvfile1, fieldnames=header)
                    writeobj.writerow(info_dic)
                    print('success')
            else:
                tag = classify(keys)
                if len(text) == 0:
                    with open('wrongkey.txt', 'a+', encoding='utf-8') as f2:
                        f2.write(filename[i])
                else:
                    if len(finavalidaddress) != 0:
                        info_dic['bitcoin'] = finavalidaddress
                        info_dic['name'] = filename[i].replace('.html', '')
                        info_dic['title'] = title
                        info_dic['classify'] = tag
                        # info_dic['keys'] = re.sub('[0-9]', '', str(keys)).replace("[('", '').replace("'", '').replace('), (', '').replace(', .)]', '').replace('.', '')
                        csvfile = open('validtransactionbtcinfo.csv', 'a+', encoding='utf-8-sig', newline='')
                        writeobj = csv.DictWriter(csvfile, fieldnames=header)
                        writeobj.writerow(info_dic)
                        print('successsuccess')
        except:
            with open('wrongfile2.txt', 'a+', encoding='utf-8') as f:
                f.write(filename[i] + '\n')
            print('false')
            continue


if __name__ == '__main__':
    get_info(file_names)