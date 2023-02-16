with open('only_graph_adjlist.txt', 'r', encoding='utf-8') as f:
    data = f.readlines()
count = {}
keylist = []

for character in data:
    # chararcters.append(character.strip())
    count.setdefault(character, 0)  # 确保了键存在于 count 字典中(默认值是 0)
    count[character] = count[character] + 1

for key,value in count.items():
    if value == 1:
        keylist.append(key)
for lines in keylist:
    with open('isolatenode.txt', 'a+', encoding='utf-8') as f:
        f.write(lines.strip() +'\n')


