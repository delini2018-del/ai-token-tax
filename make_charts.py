import json, os
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
R = json.load(open("results/results.json")); os.makedirs("charts", exist_ok=True)
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 12, "axes.spines.top": False, "axes.spines.right": False})
INK, RED, AMB, BLUE, GREY, TEAL = "#1f2937", "#c2410c", "#e9a23b", "#2563eb", "#cbd5e1", "#0f766e"
O, C = "GPT-4o o200k (2024)", "GPT-4 cl100k (2023)"

# 1 ── Article 1, same sentence, token counts
a1 = R["article1"]["counts"]; langs = ["English", "French", "Hindi", "Tamil", "Sinhala"]
fig, ax = plt.subplots(figsize=(11, 4.8))
for i, l in enumerate(langs):
    ax.barh(i, a1[C][l], color=GREY, height=0.62); ax.barh(i, a1[O][l], color=RED if l == "Sinhala" else BLUE, height=0.62)
    ax.text(a1[C][l] + 4, i, f"{a1[C][l]}", va="center", color="#64748b", fontsize=11)
    ax.text(a1[O][l] - 3, i, f"{a1[O][l]}", va="center", ha="right", color="white", fontsize=11, fontweight="bold")
ax.set_yticks(range(len(langs)), langs); ax.invert_yaxis(); ax.set_xlabel("Tokens needed for Article 1 of the Universal Declaration of Human Rights")
ax.legend(handles=[plt.Rectangle((0, 0), 1, 1, color=BLUE), plt.Rectangle((0, 0), 1, 1, color=GREY)],
          labels=["GPT-4o tokenizer (o200k, 2024)", "GPT-4 tokenizer (cl100k, 2023)"], frameon=False, loc="upper right")
fig.suptitle("\"All human beings are born free and equal in dignity and rights\" — but not in tokens", x=0.02, ha="left", fontsize=14, color=INK)
fig.tight_layout(); fig.savefig("charts/01_article1.png", dpi=200); plt.close(fig)

# 2 ── 40 languages: premium with GPT-4 vs GPT-4o tokenizers
p = R["premium"]; ls = sorted(p[O], key=lambda k: p[O][k])
fig, ax = plt.subplots(figsize=(11, 11))
for i, l in enumerate(ls):
    hi = l in ("Sinhala", "Tamil")
    ax.plot([p[O][l], p[C][l]], [i, i], color=RED if hi else GREY, lw=2 if hi else 1.2, zorder=1)
    ax.scatter(p[C][l], i, color="#94a3b8", s=30, zorder=2); ax.scatter(p[O][l], i, color=RED if hi else BLUE, s=55, zorder=3)
ax.set_yticks(range(len(ls)), ls); ax.set_xscale("log"); ax.axvline(1, color=INK, lw=1)
for t, l in [(1, "1×"), (2, "2×"), (4, "4×"), (8, "8×"), (16, "16×")]: pass
ax.set_xticks([1, 2, 4, 8, 16], ["1× (English)", "2×", "4×", "8×", "16×"])
for l in ("Sinhala", "Tamil"):
    i = ls.index(l); ax.text(p[C][l] * 1.08, i, f"{p[C][l]:.2f}× → {p[O][l]:.2f}×", va="center", color=RED, fontsize=11, fontweight="bold")
ax.set_xlabel("Tokens needed for the same text, relative to English (log scale)")
ax.legend(handles=[plt.Line2D([], [], marker="o", ls="", color="#94a3b8"), plt.Line2D([], [], marker="o", ls="", color=BLUE)],
          labels=["GPT-4 tokenizer (cl100k, 2023)", "GPT-4o tokenizer (o200k, 2024)"], frameon=False, loc="lower right")
fig.suptitle("The token tax shrank. It did not disappear. (UDHR Articles 1–6, 40 languages)", x=0.02, ha="left", fontsize=14, color=INK)
fig.tight_layout(); fig.savefig("charts/02_forty_languages.png", dpi=200); plt.close(fig)

# 3 ── Generations of tokenizers, Sinhala/Tamil/Hindi, plus raw bytes
gens = ["GPT-2 (2019)", "GPT-4 cl100k (2023)", "Claude 2-era (2023)", "Llama 3 (2024)", "Gemma (2024)", "GPT-4o o200k (2024)", "Gemma 3 (2025)"]
lab = ["GPT-2\n2019", "GPT-4\n2023", "Claude 2-era\n2023", "Llama 3\n2024", "Gemma\n2024", "GPT-4o\n2024", "Gemma 3\n2025"]
fig, ax = plt.subplots(figsize=(11, 5.4))
for l, c in [("Sinhala", RED), ("Tamil", AMB), ("Hindi", TEAL)]:
    ax.plot(range(len(gens)), [p[g][l] for g in gens], color=c, lw=2.6, marker="o", label=l)
    ax.text(len(gens) - 0.85, p[gens[-1]][l], f"{l} {p[gens[-1]][l]:.1f}×", color=c, va="center", fontsize=11)
for l, c in [("Sinhala", RED)]:
    ax.axhline(p["UTF-8 bytes"][l], color=c, ls=":", lw=1.5)
    ax.text(0, p["UTF-8 bytes"][l] * 1.08, f"Sinhala in raw UTF-8 bytes: {p['UTF-8 bytes'][l]:.1f}× English (what a byte-level model reads)", color=c, fontsize=10.5)
ax.axhline(1, color=INK, lw=1); ax.set_yscale("log"); ax.set_yticks([1, 2, 4, 8, 16], ["1× (English)", "2×", "4×", "8×", "16×"])
ax.set_xticks(range(len(gens)), lab, fontsize=10.5); ax.set_xlim(-0.3, len(gens) + 0.6)
ax.set_ylabel("Tokens relative to English"); ax.legend(frameon=False, loc="upper right")
fig.suptitle("Each new tokenizer charged Sinhala less. None charged it the same.", x=0.02, ha="left", fontsize=14, color=INK)
fig.tight_layout(); fig.savefig("charts/03_generations.png", dpi=200); plt.close(fig)
print("ok")
