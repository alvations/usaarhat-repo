# -*- coding: utf-8 -*-

import io, os, sys
from ast import literal_eval
from threading import Thread
from Queue import Queue

langs2links = literal_eval(io.open('europarl-links.txt', 'r').read())

moses_script_path = "/home/alvas/mosesdecoder/scripts" 

def wrapper(func, arg, queue):
  """" Wrapper class for multi-threaded functions """
  queue.put(func(arg))
  
def run_command(cmd):
    os.system(cmd)
    return

def get_prefix(src_lang, trg_lang):
    link = langs2links[src_lang, trg_lang]
    file_prefix = link.rpartition('/')[2].rpartition('.')[0].partition('.')[0]
    return 'Europarl.'+file_prefix

def tokenize_europarl_cmd_single(lang, prefix, infile_path='corpus.org', 
                                 outfile_path='corpus.tok',
                                 moses_script_path=moses_script_path, 
                                 shutup=False):
    
    # Initialize  cat with filename
    cat = "cat {d}/{i}/{p}.{l} |".format(d=os.getcwd(), i=infile_path, 
                                         p=prefix, l=lang)
    perl = "perl {m}/tokenizer/tokenizer.perl -l {l}".format(m=moses_script_path, l=lang)
    outfile = " > {d}/{o}/train.tok.{l}".format(d=os.getcwd(), 
                                                o=outfile_path, l=lang)
    cmd = "sh -c '{} {} {}'".format(cat, perl, outfile)
    if shutup:
        cmd = cmd + ">/dev/null 2>&1 &"
    return [cmd]

def tokenize_europarl_cmd(src_lang, trg_lang, infile_path='corpus.org', 
                          outfile_path='corpus.tok',
                          moses_script_path=moses_script_path, shutup=False):
    # Get Europarl prefix
    prefix = get_prefix(src_lang, trg_lang)
    src_cmd = tokenize_europarl_cmd_single(src_lang, prefix, infile_path, 
                                           outfile_path, moses_script_path, 
                                           shutup)
    trg_cmd = tokenize_europarl_cmd_single(trg_lang, prefix, infile_path, 
                                           outfile_path, moses_script_path, 
                                           shutup)
    
    script_lines = ["\n"] +  ["# Tokenizing Europarl "+src_lang+'-'+trg_lang]
    script_lines += src_cmd + trg_cmd
    return script_lines 
    

def tokenizer_command(lang, prefix, shutup=True):
    cat = "cat {d}/corpus.org/{p}.{l} |".format(d=os.getcwd(), p=prefix, l=lang)
    perl = "perl {m}/tokenizer/tokenizer.perl -l {l}".format(m=moses_script_path, l=lang)
    outfile = " > {d}/corpus.tok/train.tok.{l}".format(d=os.getcwd(), l=lang)
    cmd = "sh -c '{} {} {}'".format(cat, perl, outfile)
    if shutup:
        cmd = cmd + ">/dev/null 2>&1"
    return cmd
    
def tokenize_europarl(src_lang, trg_lang, shutup=True):
    file_prefix = get_prefix(src_lang, trg_lang)
    # Create a new directory to store the tokenized version of the corpus
    print "Preprocessing Europarl and saving to corpus.tok/ directory"
    os.system('mkdir corpus.tok')
    
    tokenize_src_cmd = tokenizer_command(src_lang, file_prefix, shutup=shutup)
    tokenize_trg_cmd = tokenizer_command(trg_lang, file_prefix, shutup=shutup)
    print
    print "$ " + tokenize_src_cmd
    print "$ " + tokenize_trg_cmd 
    print
    print "Be patient, you must. Tokenizing, it is..."
    
    # Tokenizing data.
    q1, q2 = Queue(), Queue()
    Thread(target=wrapper, 
           args=(run_command, tokenize_src_cmd , q1)
           ).start() 
    Thread(target=wrapper, 
           args=(run_command, tokenize_trg_cmd, q2)
           ).start() 
    q1.get(); q2.get()
    
def train_truecase_model(src_lang, trg_lang):
    pass
    
def main(src_lang, trg_lang):
    tokenize_europarl(src_lang, trg_lang, shutup=True)
    
if __name__ == '__main__':
    if len(sys.argv) < 3:
        sys.stderr.write('Usage: python %s source_lang target_lang '
                     '\n' % sys.argv[0])
        sys.exit(1)
    main(*sys.argv[1:])

