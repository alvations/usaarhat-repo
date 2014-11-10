
**How to tokenize text with Moses toolkit?**

```
MOSES_SCRIPT=/home/usaarhat/mosesdecoder/scripts

echo """„Frau Präsidentin! Ist meine Stimme mitgezählt worden?"""
echo """„Frau Präsidentin! Ist meine Stimme mitgezählt worden?""" | perl ${MOSES_SCRIPT}/tokenizer/tokenizer.perl -l de

echo """„Frau Präsidentin! Ist meine Stimme mitgezählt worden?""" > test.in
cat test.in | perl ${MOSES_SCRIPT}/tokenizer/tokenizer.perl -l de > test.out
cat test.out
```
