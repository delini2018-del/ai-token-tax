"""Count tokens for UDHR Articles 1-6 in 40 languages with 7 real tokenizers; compute the 'token premium'
(tokens needed relative to English for the same text) plus UTF-8 bytes and characters."""
import json, subprocess
T = json.load(open("data/udhr_articles_1_6.json"))
counts = json.loads(subprocess.run(["node", "tok/count.mjs"], input=json.dumps(T), capture_output=True, text=True).stdout)
counts["UTF-8 bytes"] = {k: len(v.encode()) for k, v in T.items()}
counts["Characters"] = {k: len(v) for k, v in T.items()}
prem = {tk: {k: v / c["English"] for k, v in c.items()} for tk, c in counts.items()}
# Article 1 alone, for the opening example
first = {k: v.split("\n")[0] for k, v in T.items() if k in ("English", "Sinhala", "Tamil", "Hindi", "French")}
c1 = json.loads(subprocess.run(["node", "tok/count.mjs"], input=json.dumps(first), capture_output=True, text=True).stdout)
json.dump(dict(counts=counts, premium=prem, article1=dict(text=first, counts=c1)), open("results/results.json", "w"), ensure_ascii=False, indent=1)
tks = list(counts)
print(f"{'':18s}" + "".join(f"{t[:12]:>13s}" for t in tks))
for k in sorted(T, key=lambda k: prem["GPT-4o o200k (2024)"][k]):
    print(f"{k:18s}" + "".join(f"{prem[t][k]:13.2f}" for t in tks))
print(json.dumps(c1, ensure_ascii=False)); print(first["Sinhala"])
