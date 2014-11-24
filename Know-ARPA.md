Our second Hack and Tell will go through a major component in machine translation, i.e. language modeling.

First let's take a look at a sample language model that is available from `moses`:

```
cd
wget http://www.statmt.org/moses/download/sample-models.tgz
tar xzf sample-models.tgz
cd sample-models/lm
ls
```

You will see the `europarl.srilm.gz` file, to read the file, use:

```
zcat europarl.srilm.gz | less
```

You should now see something like this:

```
\data\
ngram 1=37344
ngram 2=715602
ngram 3=495669

\1-grams:
-2.701261       !       -1.861745
-2.99693        "       -0.4159814
-5.711829       #       -0.1482528
```

To scroll down, press `enter` or `PgDn`/`PageDown` key.

To quit viewing the language model file, press `ctr + c` or press `q` and then `enter`.

The format of the file you've just seen is call the `.arpa` format. To know more about the format, see http://stackoverflow.com/questions/16408163/arpa-language-model-documentation

The `.arpa` file starts with the number of ngrams extracted and this number is useful when trying to normalize scores for your language model. For instance the snippet below states that the language model toolkit had extract 37,344 unigrams, 715,602 bigrams and 495,669 trigrams:

```
\data\
ngram 1=37344
ngram 2=715602
ngram 3=495669
```

Following with the `.arpa` file will list the ngrams one by one and for each line, you will see three columns, that refers to 

 - negative logarithmic probability of ngram
 - backoff probability of the ngram
 
Now try:

```
zgrep '\\2-grams' europarl.srilm.gz -A3 -B4
```

The above `zgrep` command search through the `.arpa` file and prints the line that starts the bigrams (i.e. `\2-grams:`) with 3 lines after it (i.e. `-A3` option) and 4 lines before it (i.e. `-B4` option). You should see:

```
-5.426242	�vp	-0.1482528
-4.916062	��alan	-0.2185327
-5.711829	�resund	-0.1482528

\2-grams:
-3.642242	! !	-0.2568094
-2.740354	! "
-2.733095	! '	-0.2340918
```

Now you've got used to the `.arpa` file format, go head to the next exercise on `KenLM`
