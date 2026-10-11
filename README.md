# The Same Question Costs More in Sinhala. Blame the AI's Alphabet.

Code for the Medium article. Counts tokens for Articles 1–6 of the Universal Declaration of Human Rights in
40 languages with seven real tokenizers (GPT-2, cl100k, o200k, Claude 2-era, Llama 3, Gemma, Gemma 3).

| Sinhala vs English (same text) | Premium |
|---|---|
| GPT-2 (2019) | 12.5× |
| GPT-4 cl100k (2023) | 8.7× |
| Claude 2-era (2023) | 7.4× |
| Llama 3 (2024) | 8.7× |
| Gemma (2024) | 4.1× |
| GPT-4o o200k (2024) | 2.75× |
| Gemma 3 (2025) | 2.2× |
| Raw UTF-8 bytes | 2.5× |

```bash
pip install -r requirements.txt
sh run_all.sh
```
Texts: NLTK `udhr2` (UDHR in Unicode) and, for Sinhala, NLTK `udhr`. Licence: MIT.
