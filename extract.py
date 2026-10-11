"""Extract Articles 1-6 of the Universal Declaration of Human Rights in each language.
Sources: NLTK's 'udhr2' corpus (UDHR in Unicode) for most languages; NLTK's 'udhr' corpus for Sinhala,
which udhr2 lacks (its Sinhala file is cut at about 10 KB, but Articles 1-6 are complete)."""
import json, re, unicodedata, sys
LANGS = {  # name: (file, corpus)
 "English": ("eng.txt", 2), "Sinhala": ("Sinhala-UTF8", 1), "Tamil": ("tam.txt", 2), "Hindi": ("hin.txt", 2),
 "Bengali": ("ben.txt", 2), "Telugu": ("tel.txt", 2), "Kannada": ("kan.txt", 2), "Malayalam": ("mal.txt", 2),
 "Marathi": ("mar.txt", 2), "Gujarati": ("guj.txt", 2), "Punjabi": ("pan.txt", 2), "Nepali": ("nep.txt", 2),
 "Urdu": ("urd.txt", 2), "Arabic": ("arb.txt", 2), "Persian": ("pes_1.txt", 2), "Hebrew": ("heb.txt", 2),
 "Russian": ("rus.txt", 2), "Greek": ("ell_monotonic.txt", 2), "Armenian": ("hye.txt", 2), "Georgian": ("kat.txt", 2),
 "Thai": ("tha.txt", 2), "Lao": ("lao.txt", 2), "Khmer": ("khm.txt", 2), "Burmese": ("mya.txt", 2),
 "Amharic": ("amh.txt", 2), "Chinese (Simpl.)": ("cmn_hans.txt", 2), "Japanese": ("jpn.txt", 2), "Korean": ("kor.txt", 2),
 "Vietnamese": ("vie.txt", 2), "Indonesian": ("ind.txt", 2), "Swahili": ("swh.txt", 2), "Yoruba": ("yor.txt", 2),
 "Hausa": ("hau_NG.txt", 2), "Igbo": ("ibo.txt", 2), "Zulu": ("zul.txt", 2), "Turkish": ("tur.txt", 2),
 "Persian": ("pes_1.txt", 2), "Hebrew": ("heb.txt", 2), "Yoruba": ("yor.txt", 2), "Chinese (Simpl.)": ("cmn_hans.txt", 2),
 "German": ("deu.txt", 2), "French": ("fra.txt", 2), "Spanish": ("spa.txt", 2), "Portuguese": ("por_BR.txt", 2), "Italian": ("ita.txt", 2),
}
def num(line):
    d = "".join(str(unicodedata.digit(ch)) for ch in line if unicodedata.digit(ch, None) is not None)
    return int(d) if d else None
KEYWORD = {"fra.txt": "Article", "por_BR.txt": "Artigo", "cmn_hans.txt": "第", "heb.txt": "סעיף", "pes_1.txt": "مادهٔ",
           "yor.txt": "Abala"}   # headings without plain digits: take the k-th heading line instead
def articles_kw(text, kw, a=1, b=7):
    lines = text.splitlines()
    hs = [i for i, l in enumerate(lines) if 0 < len(l.strip()) < 45 and l.strip().startswith(kw)]
    body = [l.strip() for l in lines[hs[a - 1] + 1:hs[b - 1]] if l.strip() and lines.index(l) not in hs]
    return "\n".join(x for x in body if not (len(x) < 45 and x.startswith(kw)))
def articles(text, a=1, b=7):
    lines = text.splitlines(); hs = {}
    for i, l in enumerate(lines):
        s = l.strip()
        if 0 < len(s) < 45 and num(s) is not None and num(s) not in hs and (not hs or num(s) == max(hs) + 1 or num(s) == 1):
            if num(s) == 1 or hs: hs[num(s)] = i
    if a not in hs or b not in hs: return None
    body = [l.strip() for l in lines[hs[a] + 1:hs[b]] if l.strip() and not (len(l.strip()) < 45 and num(l.strip()) in range(a, b))]
    return "\n".join(body)
out = {}
for name, (f, c) in LANGS.items():
    path = f"udhr2/udhr2/{f}" if c == 2 else f"udhr1/udhr/{f}"
    try: text = open(path, encoding="utf-8-sig").read()
    except FileNotFoundError: print("missing", name); continue
    t = articles_kw(text, KEYWORD[f]) if f in KEYWORD else articles(text)
    if t: out[name] = t
    else: print("no articles", name)
json.dump(out, open("data/udhr_articles_1_6.json", "w"), ensure_ascii=False, indent=1)
en = len(out["English"])
for k, v in out.items(): print(f"{k:18s} chars={len(v):5d} ratio={len(v)/en:4.2f}  {v[:50]!r}")
