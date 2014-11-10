# -*- coding: utf-8 -*-

import io, os, sys
from ast import literal_eval

langs2links = literal_eval(io.open('europarl-links.txt', 'r').read())

def download_europarl_cmd(src_lang, trg_lang, 
                          corpus_dir='corpus.org', 
                          shutup=False):
    link = langs2links[src_lang, trg_lang]
    file_prefix = link.rpartition('/')[2].rpartition('.')[0]
    corpus_dir = os.getcwd()+"/"+corpus_dir
    
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

def download_europarl(src_lang, trg_lang, shutup=False):
    link = langs2links[src_lang, trg_lang]
    file_prefix = link.rpartition('/')[2].rpartition('.')[0]
    
    # Make new directory to store the original corpus
    print "Downloading Europarl to corpus.org/ directory"
    os.system('mkdir corpus.org')
    os.chdir('corpus.org')
    
    # Download and extract the corpus from OPUS
    wget = 'wget '+link+ " -O "+link.rpartition('/')[2]
    unzip = 'unzip ' +link.rpartition('/')[2]
    
    if shutup:
         wget = wget + '>/dev/null 2>&1'
         unzip = unzip +  '>/dev/null 2>&1'
    
    print
    print "$ " + wget
    print "Be patient, you must. Downloading, it is..."
    print
    os.system(wget)
    
    print "$ " + unzip
    print "Be patient, you must. Unzipping, it is..."
    print
    os.system(unzip)
    
    print "It is finished.\n"
    
    os.chdir('..')

def main(src_lang, trg_lang, shutup=False):
    if shutup == 'shutup':
        shutup = True
    download_europarl(src_lang, trg_lang, shutup)

if __name__ == '__main__':
    if len(sys.argv) < 3:
        sys.stderr.write('Usage: python %s source_lang target_lang '
                     '\n' % sys.argv[0])
        sys.exit(1)
    main(*sys.argv[1:])
    