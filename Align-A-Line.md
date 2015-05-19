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
head -n10 Europarl.de-en.en > Europarl.de-en.10sents.en
head -n10 Europarl.de-en.de > Europarl.de-en.10sents.de
```

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


To align the words:

```
perl train-model.perl \
--root-dir .  \
--model-dir model \
--corpus Europarl.de-en.10sents \
--f en --e de  \
--external-bin-dir "training-tools" \
--mgiza -mgiza-cpus 4 \
--parallel \
--first-step 1 --last-step 3 \
>& giza.log
```
