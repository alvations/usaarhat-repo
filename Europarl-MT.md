After you have finised the exercerise from `MeeT-Moses.md`, try out this experimental script generator that can automatically generate the commands that you typed line by line previously:

Only try these exercises if you have completed the `Getting-Started.md` and `MeeT-Moses.md` !!!
For this exercise, please use the EXPERT server access so that you don't blast your laptop with hugh amount of data when you download the Europarl corpora.

```
cd 
cd usaarhat-repo/europarl-mt
ls
```

You will see multiple python scripts with extension (`.py`) and read them if you like pythonic stuff, if not just ignore all of them and focus on the `script_europarl_mt.py`

Use your favorite text editor and read the `script_europarl_mt.py`, if you like to read it from your internet browser, simply go to https://github.com/alvations/usaarhat-repo/blob/master/europarl-mt/script_europarl_mt.py

Run the python script and see the output you get:

```
python script_europarl_mt.py
```

You will see the following output:

```
#!/bin/bash


MOSES_SCRIPT=/home/usaarhat/mosesdecoder/scripts
EXPERIMENT=/home/usaarhat/git/usaarhat-repo/europarl-mt/europarl_pbsmt_en_de


mkdir europarl_pbsmt_en_de
cd europarl_pbsmt_en_de


# Downloadings Europarl en-de
mkdir ${EXPERIMENT}/corpus.org
cd ${EXPERIMENT}/corpus.org
wget http://opus.lingfil.uu.se/download.php?f=Europarl/de-en.txt.zip -O de-en.txt.zip
unzip de-en.txt.zip
cd ..
mkdir corpus.tok


# Tokenizing Europarl en-de
sh -c 'cat ${EXPERIMENT}/corpus.org/Europarl.de-en.en | perl ${MOSES_SCRIPT}/tokenizer/tokenizer.perl -l en  > ${EXPERIMENT}/corpus.tok/Europarl.de-en.tok.en' &
sh -c 'cat ${EXPERIMENT}/corpus.org/Europarl.de-en.de | perl ${MOSES_SCRIPT}/tokenizer/tokenizer.perl -l de  > ${EXPERIMENT}/corpus.tok/Europarl.de-en.tok.de' &
wait


# Training Truecaser Europarl en-de
perl ${MOSES_SCRIPT}/recaser/train-truecaser.perl --model ${EXPERIMENT}/corpus.tok/truecase-model.en --corpus ${EXPERIMENT}/corpus.tok/Europarl.de-en.tok.en &
perl ${MOSES_SCRIPT}/recaser/train-truecaser.perl --model ${EXPERIMENT}/corpus.tok/truecase-model.de --corpus ${EXPERIMENT}/corpus.tok/Europarl.de-en.tok.de &
wait


# Copying Europarl en-de for language model
cp ${EXPERIMENT}/corpus.tok/Europarl.de-en.tok.truecase.en > ${EXPERIMENT}/corpus.tok/train-all.en
cp ${EXPERIMENT}/corpus.tok/Europarl.de-en.tok.truecase.de > ${EXPERIMENT}/corpus.tok/train-all.de


# Cleaning Europarl en-de
cd ${EXPERIMENT}/corpus.tok
perl ${MOSES_SCRIPT}/training/clean-corpus-n.perl Europarl.de-en.tok.truecase en de train-clean 1 80
cd ..

```

The above output looks very similar to the line by line commands that you've entered from the `MeeT-Moses.md` exercise. What happened is that the `script_europarl_mt.py` automatically creates the script that is necessary for preprocessing the corpus before training a machine translation model with Moses.

Generate the file again with the python script and put it into an output file, e.g. `prepare_corpus.sh`.
Then view the `prepare_corpus.sh` in your fav text editor, e.g. `gedit prepare_corpus.sh`

```
python script_europarl_mt.py > prepare_corpus.sh
gedit prepare_corpus.sh
```

Now, view the `script_europarl_mt.py` in your favorite text editor, e.g. `gedit script_europarl_mt.py`.

You will see that there are multiple steps that you took similar to the `MeeT-Moses.md` exercise. In addition, there is an extra step that will download the Europarl automatically.

Take note of these parameters in the file:

```
expname = "europarl_pbsmt_en_de"
src_lang = "en"
trg_lang = "de"
```

Change the values of the above parameters in the `script_europarl_mt.py` with these value, e.g.s:

```
expname = "europarl_experiment_fr_de"
src_lang = "fr"
trg_lang = "de"
```

Then run the python script again:

```
python script_europarl_mt.py
```

Note the difference in the script, the languages has changed and so has the experiment name.

Now run the python script again and save into your own `prepare.sh` file, e.g.:

```
python script_europarl_mt.py > prepare_liling.sh
bash prepare_liling.sh
```

You will now see the corresponding steps that are taking place to process the Europarl data.
Go take make coffee and come back 15-30 mins later.

Now use list directory and you will see that a new directory with the experiment name you've given is created:

```
ls
```

Go into the new directory and see that the `corpus.org` and `corpus.tok` directories with the different text files created. For e.g. to view the file:

```
cd europarl_experiment_fr_de
cd corpus.tok
ls
cat Eurparl.de-fr.tok.truecase.de | less
```

To exit the `cat` command, use `ctr + c` or `q` and then enter

----

**Congratulations!!!** 

Now you have learned several things while hacking your way till this stage:
 - how to change / list directory in linux
 - how to use simple GIT commands
 - how to prepare corpus for Machine Translation
 - What is Truecasing?
 - What is corpus cleaning in Machine Translation?

That's all for Session 1 of USaar Hack and Tell, see you in the next session https://sites.google.com/site/usaarhat/about-us !!!
