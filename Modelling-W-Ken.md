Build some LMs
====

For the following exercises, the `txt.src` is the first 1000 line of the Europarl corpus, preprocessed with the methods we've learnt from https://github.com/alvations/usaarhat-repo/blob/master/MeeT-Moses.md 

Operators vs Parameters
----

Try the following commands the see the difference, for each `.arpa` file you've built, try to spot the difference:

```
~/mosesdecoder/bin/lmplz -o 2  < txt.src > txt.arpa
cat txt.apra | less

~/mosesdecoder/bin/lmplz -o 2 --text txt.src --arpa txt_textarpa.arpa
cat txt_textarpa.arpa | less
```

You notice that there is no difference in the output files `txt.arpa` and `txt_textarpa` because they are the same commands just that 
 - one uses the standard file input/output operation on the linux terminals (i.e. `<` and `>`) and 
 - the other uses the `--text` and `--arpa` parameters defined by KenLM  

For more information, scroll down and see the **File Related Options** below. 


Unigrams, Bigrams, Trigrams, ... Manygrams
----

Let's try

```
~/mosesdecoder/bin/lmplz -o 3  < txt.src > txt.arpa
cat txt_trigrams.apra | less

~/mosesdecoder/bin/lmplz -o 4  < txt.src > txt.arpa
cat txt_fourgrams.apra | less

```
What is the difference?

Now try:

```
~/mosesdecoder/bin/lmplz -o 10  < txt.src > txt.arpa
cat txt_tengrams.apra | less
```
 
You should see an error:

```
/home/usaarhat/mosesdecoder/lm/builder/adjust_counts.cc:58 in void lm::builder::{anonymous}::StatCollector::CalculateDiscounts(const lm::builder::DiscountConfig&) threw BadDiscountException because `discounts_[i].amount[j] < 0.0 || discounts_[i].amount[j] > j'.
ERROR: 5-gram discount out of range for adjusted count 3: -0.963829
Aborted (core dumped)
```

The error means, *'for the corpus size you have, the discounting for 5grams are too low to be taken into account, so building the language model with 10grams is not posssible in KenLM'*


Pruning
----

Pruning means to remove ngrams that has less than a certain number of counts.

In KenLM, you use the `--prune` option and subsequently the list of minimum number of counts for the different order of ngrams.

```
~/mosesdecoder/bin/lmplz -o 3 --prune 0 10 < txt.src > txt_prune10.arpa
~/mosesdecoder/bin/lmplz -o 3 --prune 0 50 < txt.src > txt_prune50.arpa
~/mosesdecoder/bin/lmplz -o 3 --prune 0 10 50 < txt.src > txt_prune1050.arpa

grep '\\2-grams' -A10 -B3 txt_prune10.arpa
grep '\\3-grams' -A10 -B3 txt_prune10.arpa

grep '\\2-grams' -A10 -B3 txt_prune50.arpa
grep '\\3-grams' -A10 -B3 txt_prune50.arpa

grep '\\2-grams' -A10 -B3 txt_prune1050.arpa
grep '\\3-grams' -A10 -B3 txt_prune1050.arpa
```

See a difference?

(Note: the pruning threshold for unigrams must be set to 0)


Discount not Sale
---

KenLM implements Kneser-Ney Discount (KND) and when the KND fails the default KenLM breaks, so by setting a discount fallback when the KND fails, KenLM will use the fallback you've set and continue to build the language model based on the fallback values.

```
~/mosesdecoder/bin/lmplz -o 2 --discount_fallback=0.5 1 1.5  < txt.src > txt_discount1.arpa
~/mosesdecoder/bin/lmplz -o 2 --discount_fallback=1 1 1  < txt.src > txt_discount2.arpa
~/mosesdecoder/bin/lmplz -o 2 --discount_fallback=1 2 3  < txt.src > txt_discount3.arpa
cat txt_discount1.arpa | less
cat txt_discount2.arpa | less
cat txt_discount3.arpa | less
```

What is the difference in the language model when you set an incremental fallback (i.e. `discount1.arpa` and `discount3.arpa1`) vs a uniform fallback (i.e. `discount3.arpa`)?  

Now try:

```
~/mosesdecoder/bin/lmplz -o 2 --discount_fallback=1.5 1 0.5  < txt.src > txt_discount4.arpa
cat txt_discount5.arpa | less
```

**Why did the KenLM command fail?** 

Because the maximum discount that you can give for unigram is 1 since the sum of probability for a word is 1 and the sum of probability for bigram is 1 + 1 and same for 3grams.

```
~/mosesdecoder/bin/lmplz -o 10 < txt.src > txt_discount5.arpa
~/mosesdecoder/bin/lmplz -o 10 --discount_fallback=1.5 1 0.5  < txt.src > txt_discount5.arpa
cat txt_discount5.arpa | less
```

Ooooo, now KenLM is happy when you tell him the discount to fallback to whenever probability because too small for the higher order of ngrams. 

But we only set fallbacks for 1,2,3grams. Seems like KenLM is using the 3grams probabilities for the higher ngrams, seems logical since we don't want to overweight the higher grams.

So how about:

```
~/mosesdecoder/bin/lmplz -o 10 --discount_fallback=1 2 3 4 5  < txt.src > txt_discount6.arpa
cat txt_discount6.arpa | less
```

Awww seems like KenLM is not very happy when you give him more than 3 fallbacks... 

Collapsing?
---

```
~/mosesdecoder/bin/lmplz -o 2 < txt.src > txt_nocollapse.arpa
~/mosesdecoder/bin/lmplz -o 2 --collapse_values < txt.src > txt_collapse.arpa
cat txt_collapse.arpa
```

Note the line `-1.9595848      der     0`.

**What happen to our fallback values on the 3rd column?** 

Now look at `txt_nocollapse.arpa` and then look at the line `-1.6257969      der     -0.33378786`. Then perform some mental calculation: `-1.6257969 + -0.33378786`.

For more info, see http://kheafield.com/professional/edinburgh/rest_paper.pdf


Emulating SRILM
----

These parameters emulates SRILM outputs, for what it's worth, if you're using KenLM to get SRILM outputs, then ...

Regardless, see **Full option list** for more information on these parameters.

```
~/mosesdecoder/bin/lmplz -o 2 --interpolate_unigrams < txt.src > txt_srilm.arpa
~/mosesdecoder/bin/lmplz -o 2 --interpolate_unigrams --vocab_pad 10 < txt.src > txt_srilm_pad10.arpa
~/mosesdecoder/bin/lmplz -o 2 --interpolate_unigrams --vocab_pad 50 < txt.src > txt_srilm_pad50.arpa
cat txt_srilm.arpa | less
cat txt_srilm_pad10.arpa | less
cat txt_srilm_pad50.arpa | less
```
