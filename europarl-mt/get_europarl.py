# -*- coding: utf-8 -*-

import io, os, sys
from ast import literal_eval

langs2links = literal_eval(io.open('europarl-links.txt', 'r').read())
#links = 
#os.system('wget')


def main(src_lang, trg_lang):
    link = langs2links[src_lang, trg_lang]
    file_prefix = link.rpartition('/')[2].rpartition('.')[0]
    os.system('mkdir corpus.org')
    os.chdir('corpus.org')
    os.system('wget '+link+ " -O "+link.rpartition('/')[2])
    os.system('unzip ' +link.rpartition('/')[2])
    os.chdir('..')
    return src_lang, trg_lang, file_prefix
 
if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.stderr.write('Usage: python %s source_lang target_lang '
                     '\n' % sys.argv[0])
        sys.exit(1)
    main(*sys.argv[1:])
    