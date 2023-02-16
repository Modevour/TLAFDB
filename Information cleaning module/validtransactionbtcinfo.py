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
header = ['bitcoin', 'title', 'sort', 'name']


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
    return rank[0:10]


def classify(keylist):
    tag = ''
    keylist = re.sub('[0-9]', '', str(keylist)).replace("[('", '').replace("'", '').replace('), (', '').replace(', .)]', '').replace(
        '.', '')
    keymatch_list = []
    classify_list = [['hackers', 'hacked', 'backdoor', 'malware', 'booter', 'hacker', 'threat', 'cracking', 'debian',
                      'hacking', 'hack', 'hacks'],
                     ['cocaine', 'cannabis', 'lsd', 'meth', 'pills', 'drugs', 'drugstore', 'xanax', 'heroin', 'kamagra',
                      'crystal', 'poison', 'drug', 'psychedelics'],
                     ['porn', 'pussy', 'lolita', 'livejasmin', 'girls', 'porno', 'sex', 'bitch', 'incest', 'videos',
                      'views', 'love', 'teen'],
                     ['ammo', 'guns', 'rifles', 'firearms', 'poudriere', 'armory', 'arms', 'gun', ' pistol', 'cartridge','barrel'],
                     ['hitman', 'killer', 'hitmen', 'red', 'killing', 'kill', 'blood', 'dead', 'assassination'],
                     ['bbc', 'news'],
                     ['forum'],
                     ['ahmia', 'links', 'link', ' wiki', 'mirror'],
                     ['cards', 'scam', 'multiescrow', 'scams', 'transfer', 'btc', 'bitcoin', 'counterfeits', 'payment',
                      'money', 'skrill', 'usd', 'paypal', 'escrow', 'card', 'accounts', 'profit', 'price', 'buy',
                      'market', 'buyer', 'iphone', 'apple', 'passport', 'services', 'cashout', 'shopping', 'store',
                      'trading', 'sell'],
                     ['email', 'e-mail', 'protonmail', 'mail', 'xxmail']]
    try:
        keymatch_list = keylist.split(', ')
        for key in keymatch_list:
            index_key = keymatch_list.index(key)
            if key in classify_list[2]:
                new = keymatch_list.pop(index_key)
                keymatch_list.insert(0, new)
        for key in keymatch_list:
            index_key = keymatch_list.index(key)
            if key in classify_list[3]:
                new = keymatch_list.pop(index_key)
                keymatch_list.insert(0, new)
        for key in keymatch_list:
            index_key = keymatch_list.index(key)
            if key in classify_list[1]:
                new = keymatch_list.pop(index_key)
                keymatch_list.insert(0, new)
        for key in keymatch_list:
            if key in classify_list[0]:
                tag = 'hacking'
                break
            elif key in classify_list[1]:
                tag = 'drugs'
                break
            elif key in classify_list[2]:
                tag = 'porn'
                break
            elif key in classify_list[3]:
                tag = 'gun'
                break
            elif key in classify_list[4]:
                tag = 'kill'
                break
            elif key in classify_list[5]:
                tag = 'news'
                break
            elif key in classify_list[6]:
                tag = 'forum'
                break
            # elif key in classify_list[7]:
            #     tag = 'door'
            #     break
            elif key in classify_list[8]:
                tag = 'transaction'
                break
            elif key in classify_list[9]:
                tag = 'mail'
                break
            else:
                tag = 'other'
    except:
        tag = 'error'
    return tag


def classify_tra(title):
    tag = ''
    trade_list = [['btc', 'wallet', 'bitcoin', 'bitcoins'],
                  ['qf', 'cc', 'card', 'cards'],
                  ['money', 'cash'],
                  ['paypal']]
    title_key = []
    title_list = title.lower().split(' ')
    for word in title_list:
        title_key.append(word)
    for key in title_key:
        if key in trade_list[0]:
            tag = 'btc'
            break
        elif key in trade_list[1]:
            tag = 'card'
            break
        elif key in trade_list[2]:
            tag = 'money'
            break
        elif key in trade_list[3]:
            tag = 'paypal'
            break
        else:
            tag = 'transaction'
    return tag


def classify_other(title):
    tag = ''
    other_list = [['chat'],
                  ['search']]
    title_key = []
    title_list = title.lower().split(' ')
    for word in title_list:
        title_key.append(word)
    for key in title_key:
        if key in other_list[0]:
            tag = 'chat'
            break
        elif key in other_list[1]:
            tag = 'search'
            break
        elif len(re.findall('market', str(title_key))) != 0:
            tag = 'transaction'
            break
        elif len(re.findall('bitcoin', str(title_key))) != 0:
            tag = 'btc'
            break
        elif len(re.findall('hack', str(title_key))) != 0:
            tag = 'hack'
            break
        else:
            tag = 'other'
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
            list3 = []
            list4 = []
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
                # if len(url) == 62:
                countlist.append(url)
            countlist = list(set(countlist))
            if len(countlist) >= 20:
                if len(finavalidaddress) != 0:
                    info_dic['name'] = filename[i].replace('.html', '')
                    info_dic['title'] = title
                    info_dic['sort'] = 'door'
                    # info_dic['keys'] = re.sub('[0-9]', '', str(keys)).replace("[('", '').replace("'", '').replace('), (', '').replace(', .)]', '').replace('.', '')
                    info_dic['bitcoin'] = finavalidaddress
                    csvfile1 = open('validtransactionbtcinfo.csv', 'a+', encoding='utf-8-sig',newline='')
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
                        if tag == 'other':
                            # info_dic['sort'] = classify_other(title)
                            tag = classify_other(title)
                        if tag == 'transaction':
                            info_dic['sort'] = classify_tra(title)
                        else:
                            info_dic['sort'] = tag
                        # info_dic['keys'] = re.sub('[0-9]', '', str(keys)).replace("[('", '').replace("'", '').replace('), (', '').replace(', .)]', '').replace('.', '')
                        csvfile = open('validtransactionbtcinfo.csv', 'a+', encoding='utf-8-sig',newline='')
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


