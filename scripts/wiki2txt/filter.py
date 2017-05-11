#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Stub
'''

import argparse
import codecs
import sys

import re
FILT1 = re.compile(r'^[0-9０-９\-]*[\.．:： 　\)」/]')
FILT2 = re.compile('[©【】〖〗　〓\uFFFC￥\\¥\u2500-\u2604:：@＠]|  |ttp|ｔｔｐ')
FILT3 = re.compile('[xX\u00D7\u2715\u2716\u2717\u2718\u274C][xX\u00D7\u2715\u2716\u2717\u2718\u274C]')
FILT4 = re.compile(r'「」|『』')

TRIMMER1 = re.compile(r'[(（][^(（]*[)）]')
TRIMMER2 = re.compile(r'[\[［][^\[［]*[\]］]')
TRIMCHARS = re.compile(r'[\[［\]］(（)）]')


USELESS_CHARS = '®™'
DELETE_TABLE = str.maketrans('', '', USELESS_CHARS)

IGNORE_FC_SPANS = [
    (0x0000, 0x002F), (0x003A, 0x0040), (0x005B, 0x0060),
    (0x007B, 0x00BF), (0xFF00, 0xFF0F), (0xFF1A, 0xFF20),
    (0xFF3B, 0xFF40), (0xFF5B, 0xFF60), (0x3000, 0x300B),
    (0x3010, 0x3030), (0x3200, 0x33FF), (0x2000, 0x2E7F),
]


IGNORE_FC_CHARS = set([0x02D7, 0x058A, 0x2010, 0x2011, 0x2012, 0x2013,  # like hyphens
                       0x2043, 0x207B, 0x208B, 0x2212,  # like hyphens
                       0x2014, 0x2015, 0x2500, 0xFE63, 0xFF0D, 0xFF70,  # like choonpus
                       0x00B7, 0x2022, 0x2219, 0x22C5, 0x30FB, 0xFF65,  # middle dot
                       ])

MAX_LENGTH = 70
MIN_LENGTH = 10


def is_noise(line):
    '''
    Check whether given line is noise or not
    '''
    first_char = ord(line[0])
    if first_char in IGNORE_FC_CHARS:
        return True
    for (start, end) in IGNORE_FC_SPANS:
        if start <= first_char <= end:
            return True

    if FILT1.match(line) or FILT2.search(line) or FILT3.search(line):
        return True
    return False


def delete_all(trimmer, line):
    '''
    Delete a line
    '''
    while True:
        prev = trimmer.sub('', line)
        if prev == line:
            return line
        line = prev


def trim(line):
    '''
    Trin a line
    '''
    line = line.translate(DELETE_TABLE)
    line = delete_all(TRIMMER1, line)
    line = delete_all(TRIMMER2, line)
    if TRIMCHARS.search(line):
        return None
    if FILT4.search(line):
        return None

    return line


def operation(inf, outf, invert, notrim):
    '''
    Stub
    '''
    for line in inf:
        line = line.replace("\t", ' ')
        if is_noise(line):
            if invert:
                outf.write(line)
        else:
            if not invert:
                if not notrim:
                    line = trim(line)
                    if line is None:
                        continue
                if MIN_LENGTH <= len(line) <= MAX_LENGTH:
                    outf.write(line)


def main():
    '''
    Parse arguments
    '''
    oparser = argparse.ArgumentParser()
    oparser.add_argument("-i", "--input", dest="input", default="-")
    oparser.add_argument("-o", "--output", dest="output", default="-")
    oparser.add_argument("-v", "--invert-match", dest="invert", action="store_true", default=False)
    oparser.add_argument("--notrim", dest="notrim", action="store_true", default=False)
    opts = oparser.parse_args()

    if opts.input == "-":
        inf = sys.stdin
    else:
        inf = codecs.open(opts.input, "r", "utf8")

    if opts.output == "-":
        outf = sys.stdout
    else:
        outf = codecs.open(opts.output, "w", "utf8")
    operation(inf, outf, opts.invert, opts.notrim)


if __name__ == '__main__':
    main()
