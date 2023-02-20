import os
import re
# 需要版本matplotlib==2.2.3，decorator==4.4.2，（非重点）我用的 networkx==2.5.1，python==3.7
# 从图中找出从起始顶点到终止顶点的所有路径
# 需要解决正则不到的情况变成一个列表


file_path = 'E:\\Dataexact\\allhtml'
file_names =os.listdir(file_path)
finalist = []
dict = {}
for i in range(0,len(file_names)):
    with open(os.path.join(file_path,file_names[i]),'r',encoding='utf-8') as f:
        try:
            # print(file_names[i])
            data =f.read()
            newlist = []
            onionlink = re.findall('[0-9a-zA_Z]+\.onion',data)

            linkslist = list(set(onionlink))
            for url in linkslist:
                newurl = url.replace('\n', '')
                if len(newurl) == 62:
                    newlist.append(newurl)
                # dict[file_names[i].replace('.html','')] = finalist[i]
        except:
#     # print(file_names[i]+'出错了')
            with open('codeerrorurl.txt', 'a+', encoding='utf-8') as f:
                f.write(file_names[i].replace('.html','') + '\n')
            continue
        else:
            if len(newlist) !=0:
                for lines in newlist:
                    with open('pagerankdata.txt', 'a+', encoding='utf-8') as f:
                        f.write(file_names[i].replace('.html','') +' '+lines+'\n')
            else:
                with open('nolink.txt', 'a+', encoding='utf-8') as f:
                    f.write(file_names[i].replace('.html','') + '\n')
