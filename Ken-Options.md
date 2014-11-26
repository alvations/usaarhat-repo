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


Pruning (Not working, pls raise issue to Ken)
----

Pruning means to remove ngrams that has less than a certain number of counts.

```
~/mosesdecoder/bin/lmplz -o 2 --prune 10 < txt.src > txt_prune10.arpa
~/mosesdecoder/bin/lmplz -o 2 --prune 50 < txt.src > txt_prune50.arpa
cat txt_prune10.apra | less
cat txt_prune50.apra | less
```

See a difference?


Emulating SRILM
----

```
~/mosesdecoder/bin/lmplz -o 2 --interpolate_unigrams < txt.src > txt_srilm.arpa
~/mosesdecoder/bin/lmplz -o 2 --interpolate_unigrams=3 < txt.src > txt_srilm.arpa
~/mosesdecoder/bin/lmplz -o 2 --interpolate_unigrams --vocab_pad 10 < txt.src > txt_srilm_pad10.arpa
~/mosesdecoder/bin/lmplz -o 2 --interpolate_unigrams --vocab_pad 50 < txt.src > txt_srilm_pad50.arpa
cat txt_srilm.arpa | less
cat txt_srilm_pad10.arpa | less
cat txt_srilm_pad50.arpa | less
```

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
cat txt_nocollapse.arpa
```

**What happen to our fallback values on the 3rd column?** 



----

KenLM Options
=====

```
~/mosesdecoder/bin/lmplz
```

shows you the options of how to use KenLM, let's try to go through this a few a time:

Standard Options
====

These are standard options for Unix/Linux software that displays the help message and verbose runtime updates.

```
  -h [ --help ]                         Show this help message
  
  --verbose_header                      Add a verbose header to the ARPA file 
                                        that includes information such as token
                                        count, smoothing type, etc.
```

Speed/Memory related Options
====

Kenneth is known to like speed and compression related stuff, so you can basically ignore these options if you're not a speed monster and just want to build quality LM within a reasonable time. However if you're training a model using slower or older computers, you have to play around with these to make KenLm work.

```
  -T [ --temp_prefix ] arg (=/tmp/lm)   Temporary file prefix
  -S [ --memory ] arg (=80%)            Sorting memory
  --minimum_block arg (=8K)             Minimum block size to allow
  --sort_block arg (=64M)               Size of IO operations for sort 
                                        (determines arity)
  --block_count arg (=2)                Block count (per order)
  --vocab_estimate arg (=1000000)       Assume this vocabulary size for 
                                        purposes of calculating memory in step 
                                        1 (corpus count) and pre-sizing the 
                                        hash table
```

File Related Options
====

```
  --text arg                            Read text from a file instead of stdin
  --arpa arg                            Write ARPA to a file instead of stdout
```

When we use the command:

```
~/mosesdecoder/bin/lmplz -o 2 < txt.src > txt.arpa

```

we are saying, 


Please call the lmplz software with `-o 2` option and I want to **feed KenLM with `txt.src`** and then I want KenLM to **poop the language into `txt.arpa`**.

Instead of using `< txt.src > txt.arpa`, we could use `~/mosesdecoder/bin/lmplz -o 2 --text txt.src --arpa txt.arpa`

Options that affects your Language Model
====

The `--prune` option simply throws away ngrams that falls below a certain count, KenLM default is not to prune i.e. `--prune 0`.

```
  --prune arg                           Prune n-grams with count less than or 
                                        equal to the given threshold.  Specify 
                                        one value for each order i.e. 0 0 1 to 
                                        prune singleton trigrams and above.  
                                        The sequence of values must be 
                                        non-decreasing and the last value 
                                        applies to any remaining orders.  
                                        Unigram pruning is not implemented, so 
                                        the first value must be zero.  Default 
                                        is to not prune, which is equivalent to
                                        --prune 0.
```

The `--discount_fallback` option is used if Kneser-Ney smoothing fails.
                                        
```
  --discount_fallback [=arg(=0.5 1 1.5)]
                                        The closed-form estimate for Kneser-Ney
                                        discounts does not work without 
                                        singletons or doubletons.  It can also 
                                        fail if these values are out of range. 
                                        This option falls back to 
                                        user-specified discounts when the 
                                        closed-form estimate fails.  Note that 
                                        this option is generally a bad idea: 
                                        you should deduplicate your corpus 
                                        instead.  However, class-based models 
                                        need custom discounts because they lack
                                        singleton unigrams.  Provide up to 
                                        three discounts (for adjusted counts 1,
                                        2, and 3+), which will be applied to 
                                        all orders where the closed-form 
                                        estimates fail.
```



```
  --collapse_values                     Collapse probability and backoff into a
                                        single value, q that yields the same 
                                        sentence-level probabilities.  See 
                                        http://kheafield.com/professional/edinb
                                        urgh/rest_paper.pdf for more details, 
                                        including a proof.
```

The `--interpolate_unigrams` is used to produce SRILM like outputs

```
  --interpolate_unigrams [=arg(=1)] (=1)
                                        Interpolate the unigrams (default) as 
                                        opposed to giving lots of mass to <unk>
                                        like SRI.  If you want SRI's behavior 
                                        with a large <unk> and the old lmplz 
                                        default, use --interpolate_unigrams 0.
```

The `--vocab_pad` is used to add <unk> words into the corpus such that your corpus reach a certain mass. 

```
  --vocab_pad arg (=0)                  If the vocabulary is smaller than this 
                                        value, pad with <unk> to reach this 
                                        size. Requires --interpolate_unigrams
```



Full option list
====
The full option list for KenLM:

``` 
Builds unpruned language models with modified Kneser-Ney smoothing.

Please cite:
@inproceedings{Heafield-estimate,
  author = {Kenneth Heafield and Ivan Pouzyrevsky and Jonathan H. Clark and Philipp Koehn},
  title = {Scalable Modified {Kneser-Ney} Language Model Estimation},
  year = {2013},
  month = {8},
  booktitle = {Proceedings of the 51st Annual Meeting of the Association for Computational Linguistics},
  address = {Sofia, Bulgaria},
  url = {http://kheafield.com/professional/edinburgh/estimate\_paper.pdf},
}

Provide the corpus on stdin.  The ARPA file will be written to stdout.  Order of
the model (-o) is the only mandatory option.  As this is an on-disk program,
setting the temporary file location (-T) and sorting memory (-S) is recommended.

Memory sizes are specified like GNU sort: a number followed by a unit character.
Valid units are % for percentage of memory (supported platforms only) and (in
increasing powers of 1024): b, K, M, G, T, P, E, Z, Y.  Default is K (*1024).
This machine has 12294324224 bytes of memory.

Language model building options:
  -h [ --help ]                         Show this help message
  -o [ --order ] arg                    Order of the model
  --interpolate_unigrams [=arg(=1)] (=1)
                                        Interpolate the unigrams (default) as 
                                        opposed to giving lots of mass to <unk>
                                        like SRI.  If you want SRI's behavior 
                                        with a large <unk> and the old lmplz 
                                        default, use --interpolate_unigrams 0.
  --skip_symbols                        Treat <s>, </s>, and <unk> as 
                                        whitespace instead of throwing an 
                                        exception
  -T [ --temp_prefix ] arg (=/tmp/lm)   Temporary file prefix
  -S [ --memory ] arg (=80%)            Sorting memory
  --minimum_block arg (=8K)             Minimum block size to allow
  --sort_block arg (=64M)               Size of IO operations for sort 
                                        (determines arity)
  --block_count arg (=2)                Block count (per order)
  --vocab_estimate arg (=1000000)       Assume this vocabulary size for 
                                        purposes of calculating memory in step 
                                        1 (corpus count) and pre-sizing the 
                                        hash table
  --vocab_file arg                      Location to write a file containing the
                                        unique vocabulary strings delimited by 
                                        null bytes
  --vocab_pad arg (=0)                  If the vocabulary is smaller than this 
                                        value, pad with <unk> to reach this 
                                        size. Requires --interpolate_unigrams
  --verbose_header                      Add a verbose header to the ARPA file 
                                        that includes information such as token
                                        count, smoothing type, etc.
  --text arg                            Read text from a file instead of stdin
  --arpa arg                            Write ARPA to a file instead of stdout
  --collapse_values                     Collapse probability and backoff into a
                                        single value, q that yields the same 
                                        sentence-level probabilities.  See 
                                        http://kheafield.com/professional/edinb
                                        urgh/rest_paper.pdf for more details, 
                                        including a proof.
  --prune arg                           Prune n-grams with count less than or 
                                        equal to the given threshold.  Specify 
                                        one value for each order i.e. 0 0 1 to 
                                        prune singleton trigrams and above.  
                                        The sequence of values must be 
                                        non-decreasing and the last value 
                                        applies to any remaining orders.  
                                        Unigram pruning is not implemented, so 
                                        the first value must be zero.  Default 
                                        is to not prune, which is equivalent to
                                        --prune 0.
  --discount_fallback [=arg(=0.5 1 1.5)]
                                        The closed-form estimate for Kneser-Ney
                                        discounts does not work without 
                                        singletons or doubletons.  It can also 
                                        fail if these values are out of range. 
                                        This option falls back to 
                                        user-specified discounts when the 
                                        closed-form estimate fails.  Note that 
                                        this option is generally a bad idea: 
                                        you should deduplicate your corpus 
                                        instead.  However, class-based models 
                                        need custom discounts because they lack
                                        singleton unigrams.  Provide up to 
                                        three discounts (for adjusted counts 1,
                                        2, and 3+), which will be applied to 
                                        all orders where the closed-form 
                                        estimates fail.
```
