# -*- coding: utf-8 -*-

import io, os, sys
from ast import literal_eval

langs2links = literal_eval(io.open('europarl-links.txt', 'r').read())

def download_europarl_cmd(src_lang, trg_lang, 
                          corpus_dir='corpus.org', 
                          shutup=False):
    link = langs2links[src_lang, trg_lang]
    file_prefix = link.rpartition('/')[2].rpartition('.')[0]
    corpus_dir = "${EXPERIMENT}"+"/"+corpus_dir
    
    make_directory = 'mkdir {}'.format(corpus_dir)
    change_directory = 'cd {}'.format(corpus_dir)
    wget = 'wget {l} -O {fn}'.format(l=link, fn=link.rpartition('/')[2])
    unzip = 'unzip {fn}'.format(fn=link.rpartition('/')[2])
    return_to_dir = 'cd ..'
    
    if shutup:
         wget = wget + '>/dev/null 2>&1'
         unzip = unzip +  '>/dev/null 2>&1'
    
    bash_cmds = [make_directory, change_directory, wget, unzip, return_to_dir]

    script_lines = ["\n"] +  ["# Downloadings Europarl "+src_lang+'-'+trg_lang]
    script_lines += bash_cmds
    return script_lines 