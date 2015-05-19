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
head Eurparl.de-en.de
head Eurparl.de-en.en
head -n10 Europarl.de-en.en > Europarl.de-en.1000sents.en
head -n10 Europarl.de-en.de > Europarl.de-en.1000sents.de
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
--corpus Europarl.de-en.10sents \
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
  
 
