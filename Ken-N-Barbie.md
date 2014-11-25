
You will need to use the Kenneth Language Modelling (KenLM) toolkit for this exercise. If you have installed `mosesdecoder`, it comes packaged with the KenLM. KenLM is a.k.a. `lmplz`.

Let's start with finding where `moses` is saved (we're not referrring to the River Nile):

```
cd; locate -b "mosesdecoder" | head -n 1
```

Let's say the `mosesdecoder` directory is saved in `/home/usaarhat/mosesdecoder`, then the KenLM program is found in `/home/usaarhat/mosesdecoder/bin/lmplz`, so try:

```
~/mosesdecoder/bin/lmplz
```

To train an ngram language model, simply do:

```
~/mosesdecoder/bin/lmplz -o 2 < txt.src > txt.arpa
```

Where the `txt.src` is the preprocessed textfile (with tokenization, truecasing, cleaning) and the `txt.arpa` file is the language model file that we require for MT.

Try the following commands the see the difference

```
~/mosesdecoder/bin/lmplz -o 2 --text txt.src --arpa txt_textarpa.arpa
cat txt_textarpa.arpa | less

~/mosesdecoder/bin/lmplz -o 3  < txt.src > txt.arpa
cat txt.apra | less

~/mosesdecoder/bin/lmplz -o 2 --prune 10 < txt.src > txt_prune10.arpa
~/mosesdecoder/bin/lmplz -o 2 --prune 50 < txt.src > txt_prune50.arpa
cat txt_prune10.apra | less
cat txt_prune50.apra | less


~/mosesdecoder/bin/lmplz -o 2 --interpolate_unigrams < txt.src > txt_srilm.arpa
~/mosesdecoder/bin/lmplz -o 2 --interpolate_unigrams --vocab_pad 10 < txt.src > txt_srilm_pad10.arpa
~/mosesdecoder/bin/lmplz -o 2 --interpolate_unigrams --vocab_pad 50 < txt.src > txt_srilm_pad50.arpa
cat txt_srilm.arpa | less
cat txt_srilm_pad10.arpa | less
cat txt_srilm_pad50.arpa | less

~/mosesdecoder/bin/lmplz -o 2 --discount_fallback=arg(=0.5 1 1.5)  < txt.src > txt_discount1.arpa
~/mosesdecoder/bin/lmplz -o 2 --discount_fallback=arg(=1 1 1)  < txt.src > txt_discount2.arpa
~/mosesdecoder/bin/lmplz -o 2 --discount_fallback=arg(=1.5 1 0.5)  < txt.src > txt_discount3.arpa
cat txt_discount1.arpa | less
cat txt_discount2.arpa | less
cat txt_discount3.arpa | less


~/mosesdecoder/bin/lmplz -o 2 --collapse_values < txt.src > txt_collapse.arpa
   
```

