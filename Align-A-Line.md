Aling Align 
====

Welcome back to USAAR Hack and Tell session. This session we'll learn how to achieve word alignments with various tools. Let's start afresh by cloning the `usaarhat-repo` and re-install moses with `momo.sh`:

```
cd
git clone https://github.com/alvations/usaarhat-repo.git
cd usaarhat-repo
bash momo.sh
```

(If the above sounds Greek/Chinese to you, go to [Getting Started]( https://github.com/alvations/usaarhat-repo/blob/master/Getting-Started.md))

----
Parallel data
====

Let's get some parallel data, preprocess them as we would from our [Eurparl MT preprocessing](https://github.com/alvations/usaarhat-repo/blob/master/Europarl-MT.md) session. It's nice to do all that preprocessing and understand the steps but the easiest way is to download pre-preprocessed data from [OPUS](http://opus.lingfil.uu.se/):

```
wget http://opus.lingfil.uu.se/Europarl/wordalign/de-en/de -O Europarl.de-en.de
wget http://opus.lingfil.uu.se/Europarl/wordalign/de-en/en -O Europarl.de-en.en
head Europarl.de-en.de
head Europarl.de-en.en
head -n100 Europarl.de-en.de > Europarl.de-en.100sents.de
head -n100 Europarl.de-en.en > Europarl.de-en.100sents.en
```

**NOTE:** The file names for the parallel files must be the same and the post-fixed should be the language code you use to represent the language (it's because moses only accepts parallel corpus files with certain naming conventions).

----

GIZA++ Addiction
====

The most addictive word alignment tool is `GIZA++` and `MGIZA++` because it's deeply integrated into the popular `Moses` MT system. The easiest way to get them is **NOT** to download, compile and install them from scratch, simply download from http://www.statmt.org/moses/RELEASE-3.0/binaries/

For linux:

```
cd
cd usaarhat-repo
wget -r --no-parent http://www.statmt.org/moses/RELEASE-3.0/binaries/linux-64bit/training-tools/
mv www.statmt.org/moses/RELEASE-3.0/binaries/linux-64bit/training-tools/ .
rm training-tools/index*
rm -rf www.statmt.org/
```

For Mac:

```
cd
cd usaarhat-repo
http://www.statmt.org/moses/RELEASE-3.0/binaries/macosx-yosemite/training-tools/
mv www.statmt.org/moses/RELEASE-3.0/binaries/macosx-yosemite/training-tools/ .
rm training-tools/index*
rm -rf www.statmt.org/
chmod -R training-tools/*
```

Train-model.perl
====

Although it's nice to go through the `GIZA++` tutorial and understand the steps of how to call the different components but the simplest way to get a word alignment trained is to use `train-model.perl` from Moses. 

```
cd ~/usaarhat-repo
perl ~/mosesdecoder/scripts/training/train-model.perl
```

You will see the following horrendous error that makes absolutely no sense to users but it's easily identifiable if you have gone through the [Moses rite of passage](http://www.statmt.org/moses/?n=FactoredTraining.HomePage) (but it's absolutely not necessary, unless you want to know about the intricate details of` moses`, which is pretty fun stuff if you like this sort of things)

```
Using SCRIPTS_ROOTDIR: /home/alvas/mosesdecoder/scripts
Use of uninitialized value $_EXTERNAL_BINDIR in concatenation (.) or string at /home/alvas/mosesdecoder/scripts/training/train-model.perl line 357.
Use of uninitialized value $_EXTERNAL_BINDIR in concatenation (.) or string at /home/alvas/mosesdecoder/scripts/training/train-model.perl line 358.
Use of uninitialized value $_EXTERNAL_BINDIR in concatenation (.) or string at /home/alvas/mosesdecoder/scripts/training/train-model.perl line 365.
Use of uninitialized value $_EXTERNAL_BINDIR in concatenation (.) or string at /home/alvas/mosesdecoder/scripts/training/train-model.perl line 366.
Use of uninitialized value $_EXTERNAL_BINDIR in concatenation (.) or string at /home/alvas/mosesdecoder/scripts/training/train-model.perl line 368.
Using single-thread GIZA
using gzip 
Use of uninitialized value $_EXTERNAL_BINDIR in concatenation (.) or string at /home/alvas/mosesdecoder/scripts/training/train-model.perl line 479.
ERROR: Cannot find mkcls, GIZA++/mgiza, & snt2cooc.out/snt2cooc in .
You MUST specify the parameter -external-bin-dir at /home/alvas/mosesdecoder/scripts/training/train-model.perl line 479.
```

There are 9 steps in Moses to build an MT model but for word alignment, what you really need is step 1 to step 3. To view the steps:

```
~/mosesdecoder/scripts/training/train-model.perl --steps
```

There steps are:

```
Unknown option: steps
Train Phrase Model

Steps: (--first-step to --last-step)
(1) prepare corpus
(2) run GIZA
(3) align words
(4) learn lexical translation
(5) extract phrases
(6) score phrases
(7) learn reordering model
(8) learn generation model
(9) create decoder config file
```

Atlas, Word Alignments
====

To get word alignments, the simplest way to get it with `GIZA++` is using the following command:

```
cd ~/usaarhat-repo

perl ~/mosesdecoder/scripts/training/train-model.perl \
--root-dir work.en-de  \
--model-dir work.en-de/model \
--corpus Europarl.de-en.100sents \
--f en --e de  \
--external-bin-dir "training-tools" \
--mgiza -mgiza-cpus 4 \
--parallel \
--first-step 1 --last-step 3
```

The parameters are:
 - **--root-dir** : specifies the working directory that you save your output files
 - **--model-dir**: specifies the directory that saves your aligned model files
 - **--corpus**: specifies the prefix name for the corpus
 - **--f**: specifies the source language 
 - **--e**: specifies the target language 
 - **--external-bin-dir**: specifies the directory where you save the `training-tools`
 - **--mgiza -mgiza-cpus 4**: specifies the usage of `MGIZA++` and the use of 4 CPUs 
 - **--parallel**: it's sort of a hack to use parallel processors for some steps (see [Moses Factored Training](http://www.statmt.org/moses/?n=FactoredTraining.HomePage)) 
 - **--first-step 1 --last-step 3**: specifies the steps to take during the `train-model.perl` process
  
 
Now, let's see the output:

```
cd work.en-de/model
less aligned.grow-diag-final
```

You will see something like these:

```
0-0 1-0 2-1 3-2
0-0 1-1 2-1 3-2 2-3 10-3 2-4 2-6 30-6 2-7 13-7 14-7 2-8 9-8 4-9 26-9 5-10 27-10 6-11 28-11 7-12 37-12 8-13 38-13 15-14 38-14 38-15 35-16 11-17 17-17 11-18 11-19 18-19 20-19 11-20 19-20 12-21 21-21 12-22 22-22 12-23 23-23 16-24 31-25 25-26 32-27 24-28 33-28 34-29 35-29 36-29 36-30 37-30 29-31 36-31 38-31 39-32
```

Each line represents the alignment points between the `Europarl.de-en.100sents.en` and `Europarl.de-en.100sents.de` lines. Let's look at the first sentence:

```
cd ~/usaarhat-repo && head -n1 Europarl.de-en.en && head -n1 Europarl.de-en.de && head -n1 work.en-de/model/aligned.grow-diag-final
```

[out]:

```
resumption of the session 
Wiederaufnahme der Sitzungsperiode 
0-0 1-0 2-1 3-2
```
 

 - The 0th word from the source language (EN), i.e. *resumption*, aligns with the 0th word from the target language (DE), i.e. *Wiederaufnahme*. 
 - The 1st word from EN, i.e. *of*, aligns with the 0th word from DE, i.e. *Wiederaufnahme*.
 - The 2nd word from EN, i.e. *the*, aligns with the 1st word from DE, , i.e. *der*
 - The 3rd word from EN aligns, i.e. *session*, with the 2nd word from DE, i.e. *Sitzungsperiode*


This is what typically known as the GDFA alignments (I'm sure there are other explanation to the algorithm to generate GDFA but the `NLTK` implementation is straight-forward, see https://github.com/nltk/nltk/blob/develop/nltk/align/gdfa.py).

Congratulations, you have successfully becomed a GIZA++ addiction!!!
