# -*- coding: utf-8 -*-

import io, os, sys
from ast import literal_eval

langs2links = literal_eval(io.open('europarl-links.txt', 'r').read())

moses_script_path = "/home/alvas/mosesdecoder/scripts" 

def get_prefix(src_lang, trg_lang, holdout=None):
    link = langs2links[src_lang, trg_lang]
    file_prefix = link.rpartition('/')[2].rpartition('.')[0].partition('.')[0]
    if holdout:
        return 'Europarl.'+file_prefix+'.all-'+str(holdout)
    else:
        return 'Europarl.'+file_prefix


############################################################################
# Tokenization command
############################################################################

def tokenize_europarl_cmd_single(lang, prefix, infile_path='corpus.org', 
                                 outfile_path='corpus.tok',
                                 moses_script_path=moses_script_path,
                                 experiment_path=os.getcwd(), shutup=False):
    
    # Initialize  cat with filename
    cat = "cat {d}/{i}/{p}.{l} |".format(d=experiment_path, i=infile_path, 
                                         p=prefix, l=lang)
    perl = "perl {m}/tokenizer/tokenizer.perl -l {l}".format(m=moses_script_path, l=lang)
    outfile = " > {d}/{o}/{p}.tok.{l}".format(d=experiment_path, 
                                              o=outfile_path, p=prefix, 
                                              l=lang)
    cmd = "{} {} {}".format(cat, perl, outfile)
    if shutup:
        cmd = cmd + ">/dev/null 2>&1"
    return cmd 

def tokenize_europarl_cmd(src_lang, trg_lang, infile_path='corpus.org', 
                          outfile_path='corpus.tok',shutup=False,
                          holdout=None):
    # Get Europarl prefix
    prefix = get_prefix(src_lang, trg_lang, holdout)
    src_cmd = tokenize_europarl_cmd_single(src_lang, prefix, infile_path, 
                                           outfile_path, "${MOSES_SCRIPT}", 
                                           "${EXPERIMENT}", shutup)
    trg_cmd = tokenize_europarl_cmd_single(trg_lang, prefix, infile_path, 
                                           outfile_path, "${MOSES_SCRIPT}", 
                                           "${EXPERIMENT}", shutup)
    
    script_lines = ["\n"] +  ["# Tokenizing Europarl "+src_lang+'-'+trg_lang]
    script_lines += [src_cmd]+ [trg_cmd]
    return script_lines 

############################################################################
# Train Truecaser command
############################################################################


def train_truecase_europarl_cmd_single(lang, infile_path, prefix, shutup=False):
    perl  = "perl ${MOSES_SCRIPT}/recaser/train-truecaser.perl"
    model = "--model {ip}/truecase-model.{l} --corpus {ip}/{p}.{l}".format(ip=infile_path, l=lang, p=prefix)
    train_cmd = "{} {}".format(perl, model)
    if shutup:
        train_cmd = train_cmd + ">/dev/null 2>&1"
    
    return train_cmd +" &"

def train_truecase_europarl_cmd(src_lang, trg_lang, infile_path='corpus.tok',
                                prefix=None, shutup=False, holdout=None):
    if not prefix:
        prefix = prefix = get_prefix(src_lang, trg_lang, holdout)+'.tok'        
    src_cmd = train_truecase_europarl_cmd_single(src_lang, 
                                                 "${EXPERIMENT}/"+infile_path, 
                                                 prefix, shutup)
    trg_cmd = train_truecase_europarl_cmd_single(trg_lang, 
                                                 "${EXPERIMENT}/"+infile_path,
                                                 prefix, shutup)
    
        
    script_lines = ["\n"] +  ["# Training Truecaser Europarl "+src_lang+'-'+trg_lang]
    script_lines += [src_cmd] + [trg_cmd] + ['wait']
    return script_lines

############################################################################
# Truecasing command
############################################################################


def truecase_europarl_cmd_single(lang, infile_path, prefix, shutup=False):
    perl = "${MOSES_SCRIPT}/recaser/truecase.perl"
    model = "--model {}/truecase-model.{}".format(infile_path, lang)
    inoutfile = "< {p}.{l} > {p}.truecase.{l}".format(l=lang, p=prefix)
    cmd = "{} {} {}".format(perl, model, inoutfile)
    if shutup:
        cmd = cmd + ">/dev/null 2>&1"
    
    return cmd +" &"
    

def truecase_europarl_cmd(src_lang, trg_lang, infile_path='corpus.tok',
                                prefix=None, shutup=False, holdout=None):
    if not prefix:
        prefix = prefix = get_prefix(src_lang, trg_lang, holdout)+'.tok'   
    src_cmd = truecase_europarl_cmd_single(src_lang, "${EXPERIMENT}/"+infile_path, 
                                     prefix, shutup)
    trg_cmd = truecase_europarl_cmd_single(trg_lang, "${EXPERIMENT}/"+infile_path,
                                     prefix, shutup)
    script_lines = ["\n"] +  ["# Truecasing Europarl "+src_lang+'-'+trg_lang]
    script_lines += [src_cmd] + [trg_cmd] + ['wait']
    
    script_lines+= ["\n"] +  ["# Copying Europarl "+src_lang+'-'+trg_lang+' for language model']
    script_lines+= ['cp {d}{p}.truecase.{l} > {d}train-all.{l}'.format(d="${EXPERIMENT}/corpus.tok/", l=src_lang, p=prefix)]
    script_lines+= ['cp {d}{p}.truecase.{l} > {d}train-all.{l}'.format(d="${EXPERIMENT}/corpus.tok/",l=trg_lang, p=prefix)]
    return script_lines

    
############################################################################
# Cleaning command
############################################################################

def clean_europarl_cmd(src_lang, trg_lang, infile_path='corpus.tok', 
                       minlen=1, maxlen=40, prefix =None, shutup=False, 
                       truecase=True, holdout=None):
    if not prefix:
        if truecase:
            prefix = prefix = get_prefix(src_lang, trg_lang, holdout)+'.tok'+'.truecase'
        else:
            prefix = prefix = get_prefix(src_lang, trg_lang, holdout)+'.tok'
            
    change_directory = "cd {}".format("${EXPERIMENT}/"+infile_path)
    perl = "perl {m}/training/clean-corpus-n.perl {p} {sl} {tl} train-clean {min} {max}".format(
           m="${MOSES_SCRIPT}", p=prefix, sl=src_lang, tl=trg_lang, 
           min=minlen, max=maxlen)
    
    if shutup:
        perl = perl + ">/dev/null 2>&1"
    cmd = [change_directory] + [perl]
    script_lines = ["\n"] +  ["# Cleaning Europarl "+src_lang+'-'+trg_lang]
    script_lines += cmd + ['cd ../..']
    return script_lines