# -*- coding: utf-8 -*-

import os

from get_europarl import download_europarl_cmd
from preprocess_europarl import tokenize_europarl_cmd, clean_europarl_cmd
from preprocess_europarl import train_truecase_europarl_cmd, truecase_europarl_cmd
from preprocess_europarl import get_prefix

from util import create_experiment

moses_script_path = "/home/alvas/mosesdecoder/scripts"
shutup=False

# Creates experiment
expname = "europarl_pbsmt_en_de"
script = create_experiment(expname, moses_script_path)

src_lang = 'en'
trg_lang = 'de'

original_corpus_path = 'corpus.org'
tokenize_corpus_path = 'corpus.tok'

holdout=6000

# Download Europarl
dl_europarl = download_europarl_cmd('en', 'de', 'corpus.org', 
                                    shutup=shutup, holdout=holdout) 

# Tokenize Europarl files
tk_europarl = tokenize_europarl_cmd('en', 'de', 'corpus.org', 'corpus.tok', 
                                    shutup=shutup, holdout=holdout)


# Train Truecaser Europarl files
trtc_europarl = train_truecase_europarl_cmd('en', 'de', 'corpus.tok',
                                          shutup=shutup, holdout=holdout)

# Truecase Europarl files
tc_europarl = truecase_europarl_cmd('en', 'de', 'corpus.tok', shutup=shutup, 
                                    holdout=holdout)

# Clean Europarl files
cl_europarl = clean_europarl_cmd('en', 'de', 'corpus.tok', 1, 80,  
                                 shutup=shutup, truecase=True, holdout=holdout)


script += dl_europarl + tk_europarl 
script += trtc_europarl + tc_europarl +  cl_europarl

for i in script:
    print i