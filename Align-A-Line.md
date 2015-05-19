Aling Align 
====

Welcome back to USAAR Hack and Tell session. This session we'll learn how to achieve word alignments with various tools. Let's start afresh by cloning the `usaarhat-repo`:

```
cd
git clone https://github.com/alvations/usaarhat-repo.git
```
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

To get the `train-model.perl`:


```
wget http://www.statmt.org/moses/RELEASE-3.0/binaries/linux-64bit/scripts/training/train-model.perl
wget http://www.statmt.org/moses/RELEASE-3.0/binaries/linux-64bit/scripts/training/LexicalTranslationModel.pm
```

To align the words:

```
perl train-model.perl \
--root-dir .  \
--model-dir model \
--corpus Europarl.de-en.10sents \
--f en --e de  \
--external-bin-dir ./training-tools \
--mgiza -mgiza-cpus 4 \
--parallel \
--first-step 1 --last-step 3 \
>& giza.log
```
