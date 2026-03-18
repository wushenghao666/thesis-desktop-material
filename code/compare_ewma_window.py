import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties, findfont

# 输出目录
out_dir = "./drift_compare_single"
os.makedirs(out_dir, exist_ok=True)

png_path = os.path.join(out_dir, "指数衰减与滑动窗口对比_单图.png")
svg_path = os.path.join(out_dir, "指数衰减与滑动窗口对比_单图.svg")

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
plt.rcParams["font.size"] = 16

# -----------------------------
# 1. 构造两种“历史样本影响方式”
# -----------------------------
gamma = 0.90
window_size = 12
max_lag = 40

lags = np.arange(0, max_lag + 1)

# 指数衰减：软遗忘
weights_decay = gamma ** lags
weights_decay = weights_decay / weights_decay.max()

# 滑动窗口：硬截断
weights_window = np.where(lags < window_size, 1.0, 0.0)

# -----------------------------
# 2. 绘图：单图叠加
# -----------------------------
fig, ax = plt.subplots(figsize=(8.8, 6.4))

ax.plot(lags, weights_decay, linewidth=2.6,
        label=rf'指数衰减：$\gamma={gamma}$')

ax.step(lags, weights_window, where='post', linewidth=2.6,
        label=rf'滑动窗口：$W={window_size}$')



# 注释
ax.text(1.0, 0.7,
        "指数衰减：\n越旧样本权重越小",
        fontsize=14.5, fontproperties=fp,
        bbox=dict(boxstyle="round,pad=0.28", facecolor="white", edgecolor="#888888"))

ax.text(7.0, 0.05,
        "滑动窗口：\n只保留最近 $W$ 个样本",
        fontsize=14.5, fontproperties=fp,
        bbox=dict(boxstyle="round,pad=0.28", facecolor="white", edgecolor="#C98A00"))


ax.set_xlabel("历史距离（越大表示越久远）", fontsize=18, fontproperties=fp)
ax.set_ylabel("相对样本权重", fontsize=18, fontproperties=fp)
ax.set_xlim(0, max_lag)
ax.set_ylim(-0.02, 1.08)
ax.set_xticks([0, 5, 10, 15, 20, 25, 30, 35, 40])
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