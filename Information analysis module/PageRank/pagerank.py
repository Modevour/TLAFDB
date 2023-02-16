class Graph():
    def __init__(self):
        self.linked_node_map = {}  # 邻接表
        self.PR_map = {}  # 存储不同的节点的PR值

    # 添加节点
    def add_node(self, node_id):
        if node_id not in self.linked_node_map:
            self.linked_node_map[node_id] = set({})
            self.PR_map[node_id] = 0
        else:
            print("这个节点已经存在")

    # 增加一条边
    def add_link(self, node1, node2):
        if node1 not in self.linked_node_map:
            self.add_node(node1)
        if node2 not in self.linked_node_map:
            self.add_node(node2)
        self.linked_node_map[node1].add(node2)  # 为node1添加一个邻接节点，表示ndoe2引用了node1

    # 计算pr
    def get_PR(self, path, epoch_num, d):  # 路径，迭代轮数，系数
        lines = open(path, "w+")
        for node in self.PR_map:
            self.PR_map[node] = 1
        for i in range(epoch_num):
            for node in self.PR_map:  # 遍历每一个节点
                num = sum([self.PR_map[temp_node]/(len(self.linked_node_map[temp_node])+1) for temp_node in self.linked_node_map[node]])
                self.PR_map[node] = (1 - d) + d * num
            if(i == epoch_num - 1):
                lines.write(str(self.PR_map))
            print("执行完第" +str(i) + "次迭代")

# 输入文件path每行一条边，边的两个点用空格分割，如更改，修正split，结果存储在res_path
if __name__ == '__main__':
    path = "pagerankdata.txt"  # 这个是图的文件
    res_path = "respagerank.txt"  # 这个是结果文件
    lines = open(path, "r")
    graph = Graph()
    for line in lines:
        # print(line)
        points = line.strip('\n').split(' ')
        # print(points)
        point1 = str(points[0])
        # print(point1)
        point2 = str(points[1])
        # print(point2)
        graph.add_link(point1, point2) #增加一条边
    graph.get_PR(res_path, 100, 0.85)