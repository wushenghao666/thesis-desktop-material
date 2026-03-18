import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401

def jsd_binary(p, q, eps=1e-12):
    p = np.clip(p, eps, 1 - eps)
    q = np.clip(q, eps, 1 - eps)
    P = np.array([p, 1 - p], dtype=float)
    Q = np.array([q, 1 - q], dtype=float)
    M = 0.5 * (P + Q)
    kl_pm = np.sum(P * np.log(P / M))
    kl_qm = np.sum(Q * np.log(Q / M))
    return 0.5 * (kl_pm + kl_qm)

vjsd = np.vectorize(jsd_binary)

grid = np.linspace(0.001, 0.999, 120)
X, Y = np.meshgrid(grid, grid)
Z = vjsd(X, Y)

out_dir = Path("./3d")
png_path = out_dir / "drift_adaptation_relation_3d_surface_only_large_font.png"
py_path = out_dir / "drift_adaptation_relation_3d_surface_only_large_font.py"

# Larger global font sizes
plt.rcParams.update({
    "font.size": 14,
    "axes.titlesize": 18,
    "axes.labelsize": 16,
    "xtick.labelsize": 13,
    "ytick.labelsize": 13,
})

fig = plt.figure(figsize=(10.2, 7.8))
ax = fig.add_subplot(111, projection="3d")

ax.plot_surface(X, Y, Z, rstride=2, cstride=2, linewidth=0, antialiased=True, alpha=0.82)

ax.set_xlabel(r"$P_{\mathrm{decay}}(v_1 \mid c_t)$", labelpad=16)
ax.set_ylabel(r"$P_{\mathrm{win}}(v_1 \mid c_t)$", labelpad=16)
ax.set_zlabel(r"$D_t(c)=\mathrm{JSD}(P_{\mathrm{decay}}, P_{\mathrm{win}})$", labelpad=14)
ax.tick_params(axis='both', which='major', labelsize=13)
ax.zaxis.set_tick_params(labelsize=13)
ax.view_init(elev=28, azim=-55)

plt.tight_layout()
fig.savefig(png_path, dpi=220, bbox_inches="tight")
plt.show()

code = r'''import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401

def jsd_binary(p, q, eps=1e-12):
    p = np.clip(p, eps, 1 - eps)
    q = np.clip(q, eps, 1 - eps)
    P = np.array([p, 1 - p], dtype=float)
    Q = np.array([q, 1 - q], dtype=float)
    M = 0.5 * (P + Q)
    kl_pm = np.sum(P * np.log(P / M))
    kl_qm = np.sum(Q * np.log(Q / M))
    return 0.5 * (kl_pm + kl_qm)

vjsd = np.vectorize(jsd_binary)

grid = np.linspace(0.001, 0.999, 120)
X, Y = np.meshgrid(grid, grid)
Z = vjsd(X, Y)

plt.rcParams.update({
    "font.size": 14,
    "axes.titlesize": 18,
    "axes.labelsize": 16,
    "xtick.labelsize": 13,
    "ytick.labelsize": 13,
})

fig = plt.figure(figsize=(10.2, 7.8))
ax = fig.add_subplot(111, projection="3d")

ax.plot_surface(X, Y, Z, rstride=2, cstride=2, linewidth=0, antialiased=True, alpha=0.82)

ax.set_xlabel(r"$P_{\mathrm{decay}}(v_1 \mid c_t)$", labelpad=16)
ax.set_ylabel(r"$P_{\mathrm{win}}(v_1 \mid c_t)$", labelpad=16)
ax.set_zlabel(r"$D_t(c)=\mathrm{JSD}(P_{\mathrm{decay}}, P_{\mathrm{win}})$", labelpad=14)
ax.set_title("3D relationship among decay estimate, window estimate, and drift strength", pad=18)
ax.tick_params(axis='both', which='major', labelsize=13)
ax.zaxis.set_tick_params(labelsize=13)
ax.view_init(elev=28, azim=-55)

plt.tight_layout()
plt.show()
'''
py_path.write_text(code, encoding="utf-8")

print(f"Saved plot to: {png_path}")
print(f"Saved code to: {py_path}")