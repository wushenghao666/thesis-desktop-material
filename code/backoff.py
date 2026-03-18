import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties, findfont

out_dir = "./input_aware_backoff_plot_color"
os.makedirs(out_dir, exist_ok=True)

png_path = os.path.join(out_dir, "回退混合示意图_彩色.png")
svg_path = os.path.join(out_dir, "回退混合示意图_彩色.svg")

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

k = 32
x = np.linspace(0, 128, 500)
alpha = k / (x + k)
bucket = 1 - alpha

fig, ax = plt.subplots(figsize=(9.2, 5.8))

# light region shading
ax.axvspan(0, 20, alpha=0.18, color="#4C78A8")
ax.axvspan(20, 60, alpha=0.14, color="#F2CF5B")
ax.axvspan(60, 128, alpha=0.14, color="#59A14F")

# curves
ax.plot(x, alpha, linewidth=2.8, color="#4C78A8",
        label=r'路径级权重 $\alpha(n_t)=\frac{k}{n_t+k}$')
ax.plot(x, bucket, linewidth=2.8, linestyle='--', color="#E45756",
        label=r'桶级权重 $1-\alpha(n_t)$')

# key point
ax.axvline(k, linestyle=':', linewidth=2.0, color="#7F7F7F")
ax.text(k + 2, 0.05, r'$n_t = k$', fontsize=14, fontproperties=fp)  # 从11改为14

# region labels
ax.text(8, 0.94, '冷启动阶段\n路径级统计主导', fontsize=14, fontproperties=fp,  # 从11改为14
        ha='left', va='top',
        bbox=dict(boxstyle="round,pad=0.25", facecolor="white", edgecolor="#4C78A8", alpha=0.95))
ax.text(40, 0.58, '过渡阶段\n两者共同作用', fontsize=14, fontproperties=fp,  # 从11改为14
        ha='center', va='center',
        bbox=dict(boxstyle="round,pad=0.25", facecolor="white", edgecolor="#C9A227", alpha=0.95))
ax.text(102, 0.94, '稳定阶段\n桶级统计主导', fontsize=14, fontproperties=fp,  # 从11改为14
        ha='center', va='top',
        bbox=dict(boxstyle="round,pad=0.25", facecolor="white", edgecolor="#59A14F", alpha=0.95))

# formula box
formula = (r'$P_t(v_i)=\alpha(n_t)\,P_{\mathrm{path}}(v_i\mid b,h_t)$' '\n'
           r'$+\,(1-\alpha(n_t))\,P_{\mathrm{bucket}}(v_i\mid b,h_t,z_t)$')
ax.text(69, 0.18, formula, fontsize=13,  # 从10.5改为13
        bbox=dict(boxstyle="round,pad=0.35", facecolor="#FFFDF5", edgecolor="#D4A017"))

# axes
ax.set_xlim(0, 128)
ax.set_ylim(0, 1.05)
ax.set_xlabel(r'当前桶状态样本数 $n_t$', fontsize=16, fontproperties=fp)  # 从12改为16
ax.set_ylabel('混合权重', fontsize=16, fontproperties=fp)  # 从12改为16

# legend
leg = ax.legend(frameon=True, fontsize=14, loc='center right', prop=fp)  # 从10改为14
leg.get_frame().set_edgecolor('#999999')
leg.get_frame().set_facecolor('white')

ax.set_xticks([0, 16, 32, 64, 96, 128])
ax.set_yticks(np.linspace(0, 1, 6))
ax.grid(True, linestyle=':', linewidth=0.8, alpha=0.7)

if fp:
    for label in ax.get_xticklabels() + ax.get_yticklabels():
        label.set_fontproperties(fp)
        label.set_fontsize(14)  # 设置刻度标签字体大小

plt.tight_layout()
plt.savefig(png_path, dpi=300, bbox_inches='tight')
plt.savefig(svg_path, bbox_inches='tight')
plt.close(fig)

print(f"Saved:\n{png_path}\n{svg_path}")