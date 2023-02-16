with open('respagerank.txt', 'r', encoding='utf-8') as  f:

    data =f.read().strip().replace('\n','').replace('{',' ').replace(':','').replace('}','').replace('\'','').split(',')

    for lines in data:
        pro = lines.strip()
        with open('processrespagerank.txt', 'a+', encoding='utf-8') as f:
            f.write(pro +'\n')