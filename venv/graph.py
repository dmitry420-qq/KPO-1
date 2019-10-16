import matplotlib.pyplot as plt
import matplotlib.pyplot as plg
import matplotlib.pyplot as graphic
import networkx as nx
import plotly.graph_objects as go
import numpy as np
import pydot
import random

class A():
    f = open('graphTable.txt', 'w')
    h = open('hanginTable.txt', 'w')
    r = open('random.txt', 'w')

    hierarchy_count = 0

    nodes_alpha=2

    rndArr = [0, 0, 0, 0]

    arr_hanging_nodes=[]
    arr_nodes=[]

    arr_node_on_each=[]

    alpha = 0

    alphaArr=[]

    def hierarchy_pos(G, root=None, width=1., vert_gap=0.2, vert_loc=0, xcenter=0.5):
        if not nx.is_tree(G):
            raise TypeError('cannot use hierarchy_pos on a graph that is not a tree')

        if root is None:
            if isinstance(G, nx.DiGraph):
                root = next(iter(nx.topological_sort(G)))  # allows back compatibility with nx version 1.11
            else:
                root = random.choice(list(G.nodes))
        def _hierarchy_pos(G, root, width=1., vert_gap=0.2, vert_loc=1, xcenter=0.5, pos=None, parent=None):
            if pos is None:
                pos = {root: (xcenter, vert_loc)}
            else:
                pos[root] = (xcenter, vert_loc)
            children = list(G.neighbors(root))
            if not isinstance(G, nx.DiGraph) and parent is not None:
                children.remove(parent)
            if len(children) != 0:
                dx = width / len(children)
                nextx = xcenter - width / 2 - dx / 2
                for child in children:
                    nextx += dx
                    pos = _hierarchy_pos(G, child, width=dx, vert_gap=vert_gap,
                                         vert_loc=vert_loc - vert_gap, xcenter=nextx,
                                         pos=pos, parent=root)
            return pos
        return _hierarchy_pos(G, root, width, vert_gap, vert_loc, xcenter)

    def calcGraph(n,child_start, child_end):
        count = 2;  # на этот узел с самого начала пойдет ветвь
        buf = count
        i = 1;  # счетчик узлов
        while i <= n:
            rnd = random.randint(child_start, child_end)  # генерируем рандомное число
            if (rnd == 0 and i == 1):
                rnd = child_end
            if (rnd == 0):
                A.rndArr[0] += 1
                A.arr_hanging_nodes.append(i)
                i+=1
                buf +=1
                continue
            if (rnd == 1):
                A.rndArr[1] += 1
            if (rnd == 2):
                A.rndArr[2] += 1
            if (rnd == 3):
                A.rndArr[3] += 1
            buf = count  # присваиваем буферной переменной
            while buf != (rnd + count):  # условие, необходимое для формирования rnd узлов
                if (buf > n):
                    break
                if (buf > 20):  # если число узлов больше 20, продолжаем вести таблицу без построения
                    A.f.write("({0}-{1})".format(i, buf) + ", ")
                    A.arr_nodes.append(str(i) + "-" + str(buf))
                    buf += 1
                else:
                    G.add_edge(i, buf)  # добавление узла в граф
                    A.f.write("({0}-{1})".format(i, buf) + ", ")
                    A.arr_nodes.append(str(i) + "-" + str(buf))
                    buf += 1
            A.hierarchy_count+=1
            if(buf>n):
                i += 1
                break
            count = buf
            i += 1
        for index in A.rndArr:
            A.r.write("{0}, ".format(index))
        for x in range((n+1)-i):
            A.arr_hanging_nodes.append(x+i)

G = nx.Graph()
n = 100
cycle = 0
count_node = 10
expected_value = 0
while A.nodes_alpha!=n:
    print(A.nodes_alpha)
    A.calcGraph(count_node, 0, A.nodes_alpha)
    A.alphaArr.append(count_node/(len(A.arr_hanging_nodes)))
    A.arr_node_on_each.append(A.nodes_alpha)
    G.clear()
    A.alpha = 0
    A.arr_nodes=[]
    A.arr_hanging_nodes=[]
    A.rndArr=[0,0,0,0]
    A.nodes_alpha+=1
    count_node+=1
print(A.alphaArr)
print(len(A.alphaArr))
print(A.arr_node_on_each)
print(len(A.arr_node_on_each))
graphic.plot(A.arr_node_on_each, A.alphaArr, 'r')
graphic.grid(True, linestyle='-', color='0.75')
graphic.show()
G.clear()
A.calcGraph(n, 0, 3)
for l in range(len(A.rndArr)):
    expected_value += (l*A.rndArr[l]/n)
print(expected_value)
pos = A.hierarchy_pos(G, 1)
nx.draw(G, pos=pos, with_labels=True)
print(A.arr_hanging_nodes)
A.h.write(str(A.arr_hanging_nodes))
print("count hanging={0}".format(len(A.arr_hanging_nodes)))
print(A.arr_nodes)
print("count nodes={0}".format(n))
print("alpha={0}".format(n/len(A.arr_hanging_nodes)))
plt.show()
x = [0,1,2,3]
width = 0.5
plg.bar(x,A.rndArr, width)
plg.xticks(x)
plg.show()

