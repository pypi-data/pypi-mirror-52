"""hash functions for the cubicbweb-file cube

:organization: Logilab
:copyright: 2018 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
:contact: http://www.logilab.fr/ -- mailto:contact@logilab.fr
"""

import re
import hashlib
from six import text_type


def compute_hash(value, alg):
    hashvalue = compute_row_hash(value, alg)
    if hashvalue:
        return '{%s}%s' % (alg, hashvalue)


def compute_row_hash(value, alg):
    if value is not None:
        hasher = hashlib.new(alg, value)
        return text_type(hasher.hexdigest())


def check_hash(hash_value, value):
    m = re.match('{(?P<alg>[A-Za-z0-9]+)}(?P<hash>.+)', hash_value)
    if m:
        alg = m.group('alg')
        hashhex = m.group('hash')
    else:  # bw compat, used to be sha1
        alg = 'sha1'
        hashhex = hash_value
    comphash = compute_row_hash(value, alg=alg)
    return comphash == hashhex
