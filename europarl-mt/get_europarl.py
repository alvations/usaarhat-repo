# -*- coding: utf-8 -*-

import io, os, sys
from ast import literal_eval

langs2links = literal_eval(io.open('europarl-links.txt', 'r').read())

def download_europarl_cmd(src_lang, trg_lang, 
                          corpus_dir='corpus.org', token_dir='corpus.tok',
                          shutup=False, holdout=3000):
    link = langs2links[src_lang, trg_lang]
    file_prefix = link.rpartition('/')[2].rpartition('.')[0].partition('.')[0]
    corpus_dir = "${EXPERIMENT}"+"/"+corpus_dir
    
    make_directory = 'mkdir {}'.format(corpus_dir)
    change_directory = 'cd {}'.format(corpus_dir)
    wget = 'wget {l} -O {fn}'.format(l=link, fn=link.rpartition('/')[2])
    unzip = 'unzip {fn}'.format(fn=link.rpartition('/')[2])
    return_to_dir = 'cd ..'
    
    if shutup:
         wget = wget + '>/dev/null 2>&1'
         unzip = unzip +  '>/dev/null 2>&1'
    
    bash_cmds = [make_directory, change_directory, wget, unzip]

    script_lines = ["\n"] +  ["# Downloadings Europarl "+src_lang+'-'+trg_lang]
    script_lines += bash_cmds
    if holdout:
        script_lines+= ["\n"] +  ["# Splitting Europarl "+src_lang+'-'+trg_lang]
        src_head = "head -n -{h} Europarl.{fp}.{l} > Europarl.{fp}.all-{h}.{l}".format(h=holdout, fp=file_prefix, l=src_lang)
        trg_head = "head -n -{h} Europarl.{fp}.{l} > Europarl.{fp}.all-{h}.{l}".format(h=holdout, fp=file_prefix, l=trg_lang)
        src_tail = "tail -n {h} Europarl.{fp}.{l} > Europarl.{fp}.last{h}.{l}".format(h=holdout, fp=file_prefix, l=src_lang)
        trg_tail = "tail -n {h} Europarl.{fp}.{l} > Europarl.{fp}.last{h}.{l}".format(h=holdout, fp=file_prefix, l=trg_lang)
        script_lines+= [src_head] + [trg_head] + [src_tail] + [trg_tail]
    script_lines += [return_to_dir]
    
    make_tokenized_directory =  'mkdir {}'.format(token_dir)
    
    script_lines += [make_tokenized_directory]
    return script_lines 