# -*- coding: utf-8 -*-

import os

from get_europarl import download_europarl_cmd
from preprocess_europarl import tokenize_europarl_cmd, clean_europarl_cmd
from util import create_experiment

moses_script_path = "/home/alvas/mosesdecoder/scripts"

# Creates experiment
expname = "europarl_pbsmt_en_de"
script = create_experiment(expname, moses_script_path)

# Downloads Europarl
dl_europarl = download_europarl_cmd('en', 'de', 'corpus.org') 

# Tokenize Europarl files
tk_europarl = tokenize_europarl_cmd('en', 'de', 'corpus.org', 'corpus.tok')


# Clean Europarl files
cl_europarl = clean_europarl_cmd('en', 'de', 'corpus.tok', 1, 40)


script += dl_europarl + tk_europarl + cl_europarl

for i in script:
    print i