# -*- coding: utf-8 -*-

import io
from ast import literal_eval

langs2links = literal_eval(io.open('new-europarl-links.txt', 'r').read())

