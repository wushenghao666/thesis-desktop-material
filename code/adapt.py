import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties, findfont
from matplotlib.patches import Rectangle

# 输出目录
out_dir = "./input_aware_adaptive_enable_plot"
os.makedirs(out_dir, exist_ok=True)

png_path = os.path.join(out_dir, "自适应启用示意图.png")
svg_path = os.path.join(out_dir, "自适应启用示意图.svg")

# 字体候选列表 - 与上面代码一致
font_file_candidates = [
    # Windows common CJK fonts
    os.path.join(os.environ.get("WINDIR", r"C:\Windows"), "Fonts", "msyh.ttc"),      # Microsoft YaHei
    os.path.join(os.environ.get("WINDIR", r"C:\Windows"), "Fonts", "msyhbd.ttc"),    # Microsoft YaHei Bold
    os.path.join(os.environ.get("WINDIR", r"C:\Windows"), "Fonts", "simhei.ttf"),    # SimHei
    os.path.join(os.environ.get("WINDIR", r"C:\Windows"), "Fonts", "simsun.ttc"),    # SimSun
    os.path.join(os.environ.get("WINDIR", r"C:\Windows"), "Fonts", "simkai.ttf"),    # KaiTi
    
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
    # 1) Prefer fonts Matplotlib can resolve by family name
    for name in font_name_candidates:
        try:
            _ = findfont(FontProperties(family=name), fallback_to_default=False)
            return FontProperties(family=name)
        except Exception:
            pass

    # 2) Fallback to explicit font files if present
    for p in font_file_candidates:
        if os.path.exists(p):
            return FontProperties(fname=p)

    # 3) Last resort (will likely not render CJK)
    return FontProperties()


fp = pick_cjk_font()

# Ensure Chinese text can render (fallbacks) and minus sign displays correctly
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = font_name_candidates + ["DejaVu Sans"]
plt.rcParams["font.size"] = 14  # 设置全局默认字体大小

# 阈值（示意）
n_min = 32
gamma = 0.20

# 画布
fig, ax = plt.subplots(figsize=(9.4, 6.0))
ax.set_xlim(0, 128)
ax.set_ylim(0, 0.8)

# 区域底色：仅右上角为启用区域
# 其他区域淡灰/浅色，启用区域浅绿
ax.add_patch(Rectangle((0, 0), 128, 0.8, facecolor="#F5F5F5", edgecolor="none", zorder=0))
ax.add_patch(Rectangle((n_min, gamma), 128 - n_min, 0.8 - gamma,
                       facecolor="#DFF3E3", edgecolor="none", zorder=0.1))
ax.add_patch(Rectangle((0, gamma), n_min, 0.8 - gamma,
                       facecolor="#FDEBD0", edgecolor="none", zorder=0.1))
ax.add_patch(Rectangle((n_min, 0), 128 - n_min, gamma,
                       facecolor="#FDEBD0", edgecolor="none", zorder=0.1))

# 阈值线
ax.axvline(n_min, color="#4C78A8", linestyle="--", linewidth=2.0)
ax.axhline(gamma, color="#E45756", linestyle="--", linewidth=2.0)

# 阈值标注
ax.text(n_min + 2, 0.03, r"$n_{\mathrm{path}} = n_{\min}$", fontsize=14, fontproperties=fp)
ax.text(4, gamma + 0.015, r"$IG = \gamma$", fontsize=14, fontproperties=fp)

# 区域文字
ax.text(88, 0.56, "启用输入感知预测\n同时满足样本数与信息增益门限",
        ha="center", va="center", fontsize=14, fontproperties=fp,
        bbox=dict(boxstyle="round,pad=0.3", facecolor="white", edgecolor="#59A14F"))
ax.text(16, 0.56, "样本数不足\n保持路径级预测",
        ha="center", va="center", fontsize=14, fontproperties=fp,
        bbox=dict(boxstyle="round,pad=0.25", facecolor="white", edgecolor="#C98A00"))
ax.text(88, 0.10, "信息增益不足\n保持路径级预测",
        ha="center", va="center", fontsize=14, fontproperties=fp,
        bbox=dict(boxstyle="round,pad=0.25", facecolor="white", edgecolor="#C98A00"))
ax.text(18, 0.10, "冷启动区域\n既缺少样本又缺少有效增益",
        ha="center", va="center", fontsize=14, fontproperties=fp,
        bbox=dict(boxstyle="round,pad=0.25", facecolor="white", edgecolor="#999999"))

# 公式框
formula = (r'$\mathrm{EnableInputAware}(b,h_t)=$' '\n'
           r'$\mathbf{1}\!\left[IG(b,h_t)>\gamma \;\wedge\; n_{\mathrm{path}}(b,h_t)\geq n_{\min}\right]$')
ax.text(75, 0.71, formula, fontsize=13,
        bbox=dict(boxstyle="round,pad=0.35", facecolor="#FFFDF5", edgecolor="#D4A017"))

# 坐标轴与标题
ax.set_xlabel(r'路径状态累计样本数 $n_{\mathrm{path}}(b,h_t)$', fontsize=16, fontproperties=fp)
ax.set_ylabel(r'信息增益 $IG(b,h_t)$', fontsize=16, fontproperties=fp)

# 刻度与网格
ax.set_xticks([0, 16, 32, 64, 96, 128])
ax.set_yticks([0.0, 0.1, 0.2, 0.4, 0.6, 0.8])
ax.grid(True, linestyle=':', linewidth=0.8, alpha=0.65)

# 美化
for spine in ax.spines.values():
    spine.set_linewidth(1.2)

if fp:
    for label in ax.get_xticklabels() + ax.get_yticklabels():
        label.set_fontproperties(fp)
        label.set_fontsize(14)  # 设置刻度标签字体大小

plt.tight_layout()
plt.savefig(png_path, dpi=300, bbox_inches='tight')
plt.savefig(svg_path, bbox_inches='tight')
plt.close(fig)

print(f"Saved:\n{png_path}\n{svg_path}")