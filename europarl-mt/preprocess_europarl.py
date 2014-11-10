# -*- coding: utf-8 -*-

import io, os, sys
from ast import literal_eval
from threading import Thread
from Queue import Queue

langs2links = literal_eval(io.open('europarl-links.txt', 'r').read())

moses_script_path = "/home/alvas/mosesdecoder/scripts" 


def get_prefix(src_lang, trg_lang):
    link = langs2links[src_lang, trg_lang]
    file_prefix = link.rpartition('/')[2].rpartition('.')[0].partition('.')[0]
    return 'Europarl.'+file_prefix

def tokenize_europarl_cmd_single(lang, prefix, infile_path='corpus.org', 
                                 outfile_path='corpus.tok',
                                 moses_script_path=moses_script_path,
                                 experiment_path=os.getcwd(),
                                 shutup=False):
    
    # Initialize  cat with filename
    cat = "cat {d}/{i}/{p}.{l} |".format(d=experiment_path, i=infile_path, 
                                         p=prefix, l=lang)
    perl = "perl {m}/tokenizer/tokenizer.perl -l {l}".format(m=moses_script_path, l=lang)
    outfile = " > {d}/{o}/train.tok.{l}".format(d=experiment_path, 
                                                o=outfile_path, l=lang)
    cmd = "sh -c '{} {} {}'".format(cat, perl, outfile)
    if shutup:
        cmd = cmd + ">/dev/null 2>&1 &"
    return [cmd]

def tokenize_europarl_cmd(src_lang, trg_lang, infile_path='corpus.org', 
                          outfile_path='corpus.tok', shutup=False):
    # Get Europarl prefix
    prefix = get_prefix(src_lang, trg_lang)
    src_cmd = tokenize_europarl_cmd_single(src_lang, prefix, infile_path, 
                                           outfile_path, "${MOSES_SCRIPT}", 
                                           "${EXPERIMENT}", shutup)
    trg_cmd = tokenize_europarl_cmd_single(trg_lang, prefix, infile_path, 
                                           outfile_path, "${MOSES_SCRIPT}", 
                                           "${EXPERIMENT}", shutup)
    
    script_lines = ["\n"] +  ["# Tokenizing Europarl "+src_lang+'-'+trg_lang]
    script_lines += src_cmd + trg_cmd + ['wait']
    return script_lines 
    

def clean_europarl_cmd(src_lang, trg_lang, infile_path='corpus.tok', 
                       minlen=1, maxlen=40,
                      moses_script_path=moses_script_path, 
                      shutup=False):
    # Get Europarl prefix
    prefix = get_prefix(src_lang, trg_lang)
    
    change_directory = "cd {}".format("${EXPERIMENT}/"+infile_path)
    perl = "perl {m}/training/clean-corpus-n.perl {p} {sl} {tl} train-clean {min} {max}".format(
           m="${MOSES_SCRIPT}", p=prefix,sl=src_lang, tl=trg_lang, 
           min=minlen, max=maxlen)
    
    cmd = [change_directory] + [perl]
    script_lines = ["\n"] +  ["# Cleaning Europarl "+src_lang+'-'+trg_lang]
    script_lines += cmd 
    return script_lines