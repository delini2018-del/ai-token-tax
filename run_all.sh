#!/bin/sh
set -e
mkdir -p udhr1 udhr2 && unzip -q -o corpus/udhr.zip -d udhr1 && unzip -q -o corpus/udhr2.zip -d udhr2
python extract.py > /dev/null           # UDHR Articles 1-6 in 40 languages -> data/
(cd tok && npm install --silent)        # seven real tokenizers (Node >= 18)
python measure.py                       # token counts and premiums -> results/
python make_charts.py                   # -> charts/
