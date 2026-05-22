import networkx as nx
import numpy as np
from scipy.optimize import linprog

# =========================
# 1️⃣ 建图（你需要补完整）
# =========================
G = nx.Graph()

# 示例：添加边（节点1, 节点2, 距离, 类型）
# type: "rail" or "road"

edges = [
    ("S1", "B8", 202, "road"),
    ("S2", "B8", 1200, "rail"),
    ("S3", "B9", 690, "rail"),
    ("S4", "B12", 690, "rail"),
    ("S5", "B11", 462, "road"),
    ("S6", "B15", 70, "road"),
    ("S7", "B17", 30, "road"),
]

# =========================
# 2️⃣ 运费函数
# =========================

def rail_cost(d):
    if d <= 300: return 20
    elif d <= 350: return 23
    elif d <= 400: return 26
    elif d <= 450: return 29
    elif d <= 500: return 32
    elif d <= 600: return 37
    elif d <= 700: return 44
    elif d <= 800: return 50
    elif d <= 900: return 55
    elif d <= 1000: return 60
    else:
        extra = (d - 1000 + 99) // 100
        return 60 + extra * 5

def road_cost(d):
    return 0.1 * d

# =========================
# 3️⃣ 加权建图
# =========================
for u, v, dist, t in edges:
    if t == "rail":
        cost = rail_cost(dist)
    else:
        cost = road_cost(dist)
    G.add_edge(u, v, weight=cost)

# =========================
# 4️⃣ 最短路 → 得到 c_ij
# =========================

S = ["S1","S2","S3","S4","S5","S6","S7"]
A = ["A"+str(i) for i in range(1,16)]

c = np.zeros((len(S), len(A)))

for i, s in enumerate(S):
    lengths = nx.single_source_dijkstra_path_length(G, s, weight='weight')
    for j, a in enumerate(A):
        c[i][j] = lengths.get(a, 1e6)  # 不可达设大数

# =========================
# 5️⃣ 运输问题（线性规划）
# =========================

# 供给
supply = np.array([800,800,1000,2000,2000,2000,3000])

# 单价
price = np.array([160,155,155,160,155,150,160])

# 需求（可调整）
demand = np.array([500]*15)

# 决策变量个数
n_i = len(S)
n_j = len(A)
n = n_i * n_j

# 目标函数
cost = []
for i in range(n_i):
    for j in range(n_j):
        cost.append(price[i] + c[i][j])

cost = np.array(cost)

# =========================
# 约束
# =========================

# 供给约束
A_ub = []
b_ub = []

for i in range(n_i):
    row = [0]*n
    for j in range(n_j):
        row[i*n_j + j] = 1
    A_ub.append(row)
    b_ub.append(supply[i])

# 需求约束
A_eq = []
b_eq = []

for j in range(n_j):
    row = [0]*n
    for i in range(n_i):
        row[i*n_j + j] = 1
    A_eq.append(row)
    b_eq.append(demand[j])

# =========================
# 求解
# =========================
res = linprog(cost, A_ub=A_ub, b_ub=b_ub,
              A_eq=A_eq, b_eq=b_eq,
              bounds=(0, None), method='highs')

# =========================
# 输出结果
# =========================
if res.success:
    print("最小总费用:", res.fun)

    x = res.x.reshape((n_i, n_j))
    for i in range(n_i):
        for j in range(n_j):
            if x[i][j] > 1e-3:
                print(f"{S[i]} -> {A[j]}: {x[i][j]:.2f}")
else:
    print("求解失败")