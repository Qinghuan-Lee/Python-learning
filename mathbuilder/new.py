import numpy as np
from scipy.optimize import linprog

# 目标函数系数
c = [-0.05, -0.27, -0.19, -0.185, -0.185]

# 等式约束
A_eq = [[1, 1.01, 1.02, 1.045, 1.065]]
b_eq = [1]

# 风险参数
a = 0.02

# 不等式约束
A_ub = [
    [0, 0.025, 0, 0, 0],
    [0, 0, 0.015, 0, 0],
    [0, 0, 0, 0.055, 0],
    [0, 0, 0, 0, 0.026]
]

b_ub = [a, a, a, a]

# 变量范围
bounds = [(0, None) for _ in range(5)]

# 求解
result = linprog(c, A_ub=A_ub, b_ub=b_ub,
                 A_eq=A_eq, b_eq=b_eq,
                 bounds=bounds)

print("最优解：", result.x)
print("最优目标值：", result.fun)