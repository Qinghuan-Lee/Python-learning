import matplotlib.pyplot as plt
import matplotlib
from matplotlib.patches import Ellipse, Polygon, FancyBboxPatch
import matplotlib.patheffects as pe
import numpy as np

# ── CJK 字体配置 ──
matplotlib.rcParams['font.sans-serif'] = [
    'Microsoft YaHei', 'SimHei', 'PingFang SC', 'WenQuanYi Zen Hei',
    'Noto Sans CJK SC', 'Source Han Sans CN', 'DejaVu Sans'
]
matplotlib.rcParams['axes.unicode_minus'] = False

# ── 画布 ──
fig, ax = plt.subplots(figsize=(8, 11))
fig.patch.set_facecolor('#0e0818')
ax.set_facecolor('#0e0818')
ax.set_xlim(-4.5, 4.5)
ax.set_ylim(-7.5, 6.5)
ax.set_aspect('equal')
ax.axis('off')

# ══════════════════════════════════════════════
#  背景
# ══════════════════════════════════════════════

for r, a in [(8, 0.15), (6, 0.20), (4.5, 0.25)]:
    ax.add_patch(Ellipse((0, 0.5), r, r * 1.3,
        facecolor='#1a0a30', alpha=a, edgecolor='none', zorder=0))

np.random.seed(42)
for _ in range(60):
    x = np.random.uniform(-4.2, 4.2)
    y = np.random.uniform(-7.2, 6.2)
    s = np.random.uniform(0.3, 2.5)
    a = np.random.uniform(0.05, 0.30)
    c = np.random.choice(['#FFD700', '#FFB7D5', '#9080ee', '#ffffff'])
    ax.plot(x, y, '*', color=c, markersize=s, alpha=a, zorder=0)

# ══════════════════════════════════════════════
#  绪山真寻 Mogami Mahiro
# ══════════════════════════════════════════════

# ── 头发（后层）──
ax.add_patch(Ellipse((0, 1.5), 6.0, 8.0,
    facecolor='#a05070', edgecolor='none', zorder=1))
ax.add_patch(Ellipse((0, 1.8), 5.4, 7.2,
    facecolor='#b86888', edgecolor='none', zorder=1))

# ── 头发侧缕 ──
for pts in [
    [(-2.4, 2.0), (-2.7, -1.2), (-1.9, -1.0), (-1.6, 2.0)],
    [( 1.6, 2.0), ( 1.9, -1.0), ( 2.7, -1.2), ( 2.4, 2.0)],
]:
    ax.add_patch(Polygon(pts, facecolor='#c08098', edgecolor='none', zorder=1))

# ── 脖子 ──
ax.add_patch(FancyBboxPatch((-0.4, -1.5), 0.8, 1.2,
    boxstyle="round,pad=0.1", facecolor='#ffe0c4', edgecolor='none', zorder=1.5))

# ── 脸 ──
ax.add_patch(Ellipse((0, 0.9), 3.6, 4.0,
    facecolor='#ffe0c4', edgecolor='none', zorder=2))

# ── 呆毛 ──
ax.plot([0.0, 0.3, 0.8, 0.4], [4.0, 5.0, 5.3, 4.5],
        color='#ffb7d5', linewidth=2.5, solid_capstyle='round', zorder=4)

# ── 刘海 ──
for pts, col in [
    ([(-1.7, 2.5), (-1.0, 4.3), (-0.2, 2.5)], '#ffb7d5'),
    ([(-0.5, 2.5), ( 0.1, 4.6), ( 0.6, 2.5)], '#ffc4de'),
    ([ (0.3, 2.5), ( 1.0, 4.3), ( 1.7, 2.5)], '#e8a0b8'),
    ([(-0.15,2.5), ( 0.1, 3.5), ( 0.35,2.5)], '#ffd0e8'),
]:
    ax.add_patch(Polygon(pts, facecolor=col, edgecolor='none', zorder=3))

ax.add_patch(Ellipse((-0.2, 3.7), 1.0, 0.3, angle=10,
    facecolor='#fff4f8', alpha=0.2, edgecolor='none', zorder=3.5))

# ── 眼睛 ──
for x, d in [(-0.75, -1), (0.75, 1)]:
    ax.add_patch(Ellipse((x, 1.2), 1.0, 1.2,
        facecolor='white', edgecolor='#502878', linewidth=1.0, zorder=4))
    ax.add_patch(Ellipse((x, 1.1), 0.82, 1.0,
        facecolor='#8870dd', edgecolor='none', zorder=5))
    ax.add_patch(Ellipse((x, 1.4), 0.82, 0.45,
        facecolor='#5850a8', alpha=0.4, edgecolor='none', zorder=5.3))
    ax.add_patch(Ellipse((x, 0.85), 0.5, 0.25,
        facecolor='#a898ee', alpha=0.3, edgecolor='none', zorder=5.3))
    ax.add_patch(Ellipse((x, 1.05), 0.38, 0.5,
        facecolor='#200850', edgecolor='none', zorder=6))
    # 高光
    ax.add_patch(Ellipse((x + d * 0.18, 1.5), 0.22, 0.22,
        facecolor='white', edgecolor='none', zorder=7))
    ax.add_patch(Ellipse((x - d * 0.10, 0.9), 0.10, 0.10,
        facecolor='white', edgecolor='none', zorder=7))
    # 睫毛
    ax.plot([x - 0.55, x + 0.55], [1.85, 1.85],
            color='#3a1860', linewidth=3.0, solid_capstyle='round', zorder=4)
    ax.plot([x + d * 0.45, x + d * 0.72], [1.85, 2.0],
            color='#3a1860', linewidth=2.0, solid_capstyle='round', zorder=4)

# ── 眉毛 ──
ax.plot([-1.25, -0.25], [2.30, 2.22], color='#a07888',
        linewidth=2.2, solid_capstyle='round', zorder=4)
ax.plot([ 0.25,  1.25], [2.22, 2.30], color='#a07888',
        linewidth=2.2, solid_capstyle='round', zorder=4)

# ── 鼻子 ──
ax.plot([0.02, 0.08], [0.80, 0.60], color='#d4b098', linewidth=1.3, zorder=4)

# ── 腮红 ──
for bx in [-1.1, 1.1]:
    ax.add_patch(Ellipse((bx, 0.6), 0.55, 0.22,
        facecolor='#ffb3c6', alpha=0.35, edgecolor='none', zorder=4))

# ── 嘴巴 ──
t = np.linspace(0, np.pi, 30)
ax.plot(0.20 * np.cos(t), 0.25 + 0.07 * np.sin(t),
        color='#ff6b8a', linewidth=2.0, solid_capstyle='round', zorder=4)

# ══════════════════════════════════════════════
#  制服
# ══════════════════════════════════════════════

# ── 西装外套 ──
ax.add_patch(Polygon([(-2.0, -1.4), (-0.5, -1.4), (-0.4, -3.8), (-1.8, -3.8)],
    facecolor='#1B1464', edgecolor='none', zorder=3))
ax.add_patch(Polygon([( 0.5, -1.4), ( 2.0, -1.4), ( 1.8, -3.8), ( 0.4, -3.8)],
    facecolor='#1B1464', edgecolor='none', zorder=3))

# 外套边缘描线
for pts in [
    [(-2.0,-1.4),(-0.5,-1.4),(-0.4,-3.8),(-1.8,-3.8)],
    [(0.5,-1.4),(2.0,-1.4),(1.8,-3.8),(0.4,-3.8)],
]:
    xs = [p[0] for p in pts] + [pts[0][0]]
    ys = [p[1] for p in pts] + [pts[0][1]]
    ax.plot(xs, ys, color='#281880', linewidth=0.6, zorder=3.5)

# ── 衬衫 ──
ax.add_patch(FancyBboxPatch((-0.48, -1.5), 0.96, 2.3,
    boxstyle="round,pad=0.02", facecolor='#F0EAFF', edgecolor='none', zorder=2.5))

# ── 领子 ──
ax.add_patch(Polygon([(-0.48,-1.4),(-1.0,-1.15),(-1.7,-1.4),(-0.48,-1.6)],
    facecolor='#E8E0FF', edgecolor='none', zorder=5))
ax.add_patch(Polygon([( 0.48,-1.4),( 1.0,-1.15),( 1.7,-1.4),( 0.48,-1.6)],
    facecolor='#E8E0FF', edgecolor='none', zorder=5))

# ── 红色蝴蝶结 ──
ax.add_patch(Polygon([(-0.18,-1.5),(0.18,-1.5),(0.32,-2.1),(0,-2.25),(-0.32,-2.1)],
    facecolor='#FF3050', edgecolor='#CC2040', linewidth=0.5, zorder=6))
ax.add_patch(Polygon([(-0.18,-1.5),(-0.50,-1.7),(-0.18,-1.85)],
    facecolor='#FF4060', edgecolor='none', zorder=6.5))
ax.add_patch(Polygon([( 0.18,-1.5),( 0.50,-1.7),( 0.18,-1.85)],
    facecolor='#FF4060', edgecolor='none', zorder=6.5))
ax.add_patch(Ellipse((0, -1.55), 0.12, 0.12,
    facecolor='#CC2040', edgecolor='none', zorder=7))

# ── 裙子 ──
ax.add_patch(Polygon([(-1.8,-3.8),(1.8,-3.8),(2.3,-5.3),(-2.3,-5.3)],
    facecolor='#100c40', edgecolor='#080830', linewidth=0.5, zorder=3))
for i in range(-4, 5):
    x = i * 0.3
    ax.plot([x*0.8, x*1.2], [-3.8, -5.3],
            color='#181060', linewidth=0.4, alpha=0.5, zorder=3.5)
ax.plot([-2.3, 2.3], [-5.3, -5.3], color='#281870', linewidth=1.5, zorder=3.5)

# ══════════════════════════════════════════════
#  装饰星星
# ══════════════════════════════════════════════

for sx, sy in [
    (-3.5,5.0),(3.5,4.5),(-3.8,1.5),(3.8,0.5),
    (-3.0,-3.5),(3.2,-3.0),(0,5.8),(-2.0,5.5),(2.5,5.3),
    (-3.5,-6.0),(3.5,-5.5),(-1.5,-6.5),(1.5,-6.3),
]:
    sz = np.random.uniform(0.06, 0.16)
    al = np.random.uniform(0.40, 0.85)
    co = np.random.choice(['#FFD700', '#FFB7D5', '#9080ee'])
    ax.plot([sx-sz, sx+sz], [sy, sy], color=co, lw=1.5,
            alpha=al, zorder=10, solid_capstyle='round')
    ax.plot([sx, sx], [sy-sz, sy+sz], color=co, lw=1.5,
            alpha=al, zorder=10, solid_capstyle='round')
    d = sz * 0.6
    ax.plot([sx-d, sx+d], [sy-d, sy+d], color=co, lw=0.8,
            alpha=al*0.6, zorder=10, solid_capstyle='round')
    ax.plot([sx-d, sx+d], [sy+d, sy-d], color=co, lw=0.8,
            alpha=al*0.6, zorder=10, solid_capstyle='round')

# ══════════════════════════════════════════════
#  文字
# ══════════════════════════════════════════════

ax.text(0, -6.0, '绪 山 真 寻', fontsize=24, color='#FFB7D5',
        ha='center', va='center', fontweight='bold',
        path_effects=[pe.withStroke(linewidth=3, foreground='#3a0830')], zorder=10)

ax.text(0, -6.6, 'Mogami Mahiro', fontsize=12, color='#9080ee',
        ha='center', va='center', style='italic',
        path_effects=[pe.withStroke(linewidth=2, foreground='#0e0818')], zorder=10)

ax.text(0, -7.1, '—— お兄ちゃんはおしまい！ ——', fontsize=9, color='#6850b0',
        ha='center', va='center',
        path_effects=[pe.withStroke(linewidth=1.5, foreground='#0e0818')], zorder=10)

# ══════════════════════════════════════════════
#  保存并展示
# ══════════════════════════════════════════════

plt.savefig('mahiro.png', dpi=200, facecolor='#0e0818',
            bbox_inches='tight', pad_inches=0.5)
plt.show()
print("✨ 已保存为 mahiro.png")
