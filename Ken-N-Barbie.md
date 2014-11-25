
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

Proceed to https://github.com/alvations/usaarhat-repo/blob/master/Ken-Options.md
