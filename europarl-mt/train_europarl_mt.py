# -*- coding: utf-8 -*-

import os

from get_europarl import download_europarl_cmd
from preprocess_europarl import tokenize_europarl_cmd
from util import create_experiment

script = ['#!/bin/bash']

moses_script_path = "/home/alvas/mosesdecoder/scripts" 
shutup=True

# Creates experiment
expname = "europarl_pbsmt_en_de"
create_experiment(expname)

# Downloads Europarl
dl_europarl = download_europarl_cmd('en', 'de', 'corpus.org', shutup=shutup) 
script += dl_europarl

# Tokenize Europarl files
tk_europarl = tokenize_europarl_cmd('en', 'de', 'corpus.org', 'corpus.tok', 
                                shutup=shutup)
script += tk_europarl

for i in script:
    print i