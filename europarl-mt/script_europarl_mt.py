# -*- coding: utf-8 -*-

import os

from get_europarl import download_europarl_cmd
from preprocess_europarl import tokenize_europarl_cmd, clean_europarl_cmd
from preprocess_europarl import train_truecase_europarl_cmd, truecase_europarl_cmd
from preprocess_europarl import get_prefix

from util import create_experiment, find_moses

# Automatically finds Moses directory.
moses_script_path = find_moses()

# Creates an experiment name.
expname = "europarl_pbsmt_en_de"
# Create experiments creates a folder that stores your experiment
script = create_experiment(expname, moses_script_path)

src_lang = 'en'
trg_lang = 'de'

# Ignore the holdout and shutup parameters, these are for advance uses.
holdout=None
shutup=False

# These directories stores the downloaded and processed corpus.
original_corpus_path = 'corpus.org'
tokenized_corpus_path = 'corpus.tok' 

# Download Europarl
dl_europarl = download_europarl_cmd(src_lang, trg_lang, 
                                    original_corpus_path, 
                                    shutup=shutup, holdout=holdout) 

# Tokenize Europarl files
tk_europarl = tokenize_europarl_cmd(src_lang, trg_lang, 
                                    original_corpus_path, 
                                    tokenized_corpus_path, 
                                    shutup=shutup, holdout=holdout)


# Train Truecaser Europarl files
trtc_europarl = train_truecase_europarl_cmd(src_lang, trg_lang, 
                                            tokenized_corpus_path,
                                            shutup=shutup, holdout=holdout)

# Truecase Europarl files
tc_europarl = truecase_europarl_cmd(src_lang, trg_lang,
                                    tokenized_corpus_path, 
                                    shutup=shutup, holdout=holdout)

# Clean Europarl files
cl_europarl = clean_europarl_cmd(src_lang, trg_lang,
                                 tokenized_corpus_path, 1, 80, 
                                 prefix=None, 
                                 shutup=shutup, 
                                 truecase=True, 
                                 holdout=holdout)

#cl_europarl = clean_europarl_cmd('en', 'de', 'corpus.tok', 1, 80, prefix='train-90percent', 
#                                 shutup=shutup, truecase=True, holdout=holdout)


script += dl_europarl + tk_europarl 
script += trtc_europarl + tc_europarl +  cl_europarl

for i in script:
    print i
