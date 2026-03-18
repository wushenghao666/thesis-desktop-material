import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties, findfont

# 输出目录
out_dir = "./entropy_demo_single"
os.makedirs(out_dir, exist_ok=True)

png_path = os.path.join(out_dir, "香农熵随分支确定性变化.png")
svg_path = os.path.join(out_dir, "香农熵随分支确定性变化.svg")

# 字体候选列表 - 与原代码保持一致
font_file_candidates = [
    # Windows common CJK fonts
    os.path.join(os.environ.get("WINDIR", r"C:\Windows"), "Fonts", "msyh.ttc"),
    os.path.join(os.environ.get("WINDIR", r"C:\Windows"), "Fonts", "msyhbd.ttc"),
    os.path.join(os.environ.get("WINDIR", r"C:\Windows"), "Fonts", "simhei.ttf"),
    os.path.join(os.environ.get("WINDIR", r"C:\Windows"), "Fonts", "simsun.ttc"),
    os.path.join(os.environ.get("WINDIR", r"C:\Windows"), "Fonts", "simkai.ttf"),

    # Linux common CJK fonts
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
    "/usr/share/fonts/truetype/arphic/uming.ttc",
]

font_name_candidates = [
    "Microsoft YaHei",
    "SimHei",
    "SimSun",
    "KaiTi",
    "Noto Sans CJK SC",
    "WenQuanYi Micro Hei",
    "Arial Unicode MS",
]

def pick_cjk_font() -> FontProperties:
    # 1) 优先按 family name 解析
    for name in font_name_candidates:
        try:
            _ = findfont(FontProperties(family=name), fallback_to_default=False)
            return FontProperties(family=name)
        except Exception:
            pass

    # 2) 回退到显式字体文件
    for p in font_file_candidates:
        if os.path.exists(p):
            return FontProperties(fname=p)

    # 3) 最后兜底
    return FontProperties()

fp = pick_cjk_font()

# Matplotlib 全局配置
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = font_name_candidates + ["DejaVu Sans"]
plt.rcParams["font.size"] = 16   # 原来是 14，这里调大

# -----------------------------
# 1. 香农熵函数
# -----------------------------
def entropy_binary(p):
    """
    二元分布 [p, 1-p] 的香农熵（以2为底，单位bit）
    """
    p = np.clip(p, 1e-12, 1 - 1e-12)
    q = 1.0 - p
    return -(p * np.log2(p) + q * np.log2(q))

# -----------------------------
# 2. 构造“分支确定性增强”的路径级分布
# -----------------------------
# 主分支概率 p 从 0.5 增大到 0.99
# p 越大，表示分支越确定
p_main = np.linspace(0.5, 0.99, 300)

# 路径级熵
H_path = entropy_binary(p_main)

# -----------------------------
# 3. 绘图：单图版
# -----------------------------
fig, ax = plt.subplots(figsize=(8.2, 6.2))  # 稍微放大画布，避免文字拥挤

ax.plot(p_main, H_path, linewidth=2.6, label=r'$H(P)$')

# 标注几个典型点
idx_05 = np.argmin(np.abs(p_main - 0.50))
idx_08 = np.argmin(np.abs(p_main - 0.80))
idx_095 = np.argmin(np.abs(p_main - 0.95))

ax.scatter([p_main[idx_05], p_main[idx_08], p_main[idx_095]],
           [H_path[idx_05], H_path[idx_08], H_path[idx_095]],
           s=55, zorder=3)

ax.text(0.515, 0.92,
        "接近均匀分布\n熵接近最大",
        fontsize=14.5, fontproperties=fp,
        bbox=dict(boxstyle="round,pad=0.28", facecolor="white", edgecolor="#888888"))

ax.text(0.77, H_path[idx_08] + 0.07,
        "主分支概率增大\n不确定性下降",
        fontsize=14.5, fontproperties=fp,
        bbox=dict(boxstyle="round,pad=0.28", facecolor="white", edgecolor="#C98A00"))

ax.text(0.84, H_path[idx_095] + 0.10,
        "趋于确定\n熵进一步降低",
        fontsize=14.5, fontproperties=fp,
        bbox=dict(boxstyle="round,pad=0.28", facecolor="white", edgecolor="#59A14F"))

formula = r'$H(P)=-\sum_y P(y)\log_2 P(y)$'
ax.text(0.57, 0.12, formula,
        fontsize=16,
        bbox=dict(boxstyle="round,pad=0.32", facecolor="#FFFDF5", edgecolor="#D4A017"))

ax.set_xlabel(r'主分支概率 $p$', fontsize=18, fontproperties=fp)
ax.set_ylabel('香农熵（bit）', fontsize=18, fontproperties=fp)
ax.set_xlim(0.5, 1.0)
ax.set_ylim(0.0, 1.05)
ax.set_xticks([0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
ax.set_yticks([0.0, 0.2, 0.4, 0.6, 0.8, 1.0])
ax.grid(True, linestyle=':', linewidth=0.8, alpha=0.65)
ax.legend(loc='upper right', fontsize=14, frameon=True)

# 美化
for spine in ax.spines.values():
    spine.set_linewidth(1.2)

if fp:
    for label in ax.get_xticklabels() + ax.get_yticklabels():
        label.set_fontproperties(fp)
        label.set_fontsize(15)

plt.tight_layout()
plt.savefig(png_path, dpi=300, bbox_inches='tight')
plt.savefig(svg_path, bbox_inches='tight')
plt.close(fig)

print(f"Saved:\n{png_path}\n{svg_path}")