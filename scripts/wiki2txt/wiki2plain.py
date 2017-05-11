#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Stub
'''

import argparse
import codecs
import sys

import re

HREF_RE = re.compile(r'<a href[^>]*>')


USELESS_CHARS = '\u000D\u0085\u2028\u2029'  # some line breaks
DELETE_TABLE = str.maketrans('', '', USELESS_CHARS)


def operation(inf, outf, savelink, onlylink):
    '''
    Stub
    '''
    link_start = ''
    link_end = ''
    if onlylink:
        savelink = True

    if savelink:
        link_start = '<<'
        link_end = '>>'

    for line in inf:
        if line.startswith('<') or len(line) < 5:
            continue
        line = line.translate(DELETE_TABLE)

        if savelink:
            line = line.replace(link_start, '')
            line = line.replace(link_end, '')

        line = line.replace('。', "。\n")
        line = line.replace('</a>', link_end)

        if savelink:
            line = line.replace(link_start + link_end, '')  # erase empty link

        while True:
            prev = line
            line = HREF_RE.sub(link_start, line)
            if prev == line:
                break

        if onlylink:
            lines = line.rstrip().split("\n")
            for myline in lines:
                if myline.count(link_start) == myline.count(link_end) > 0:
                    outf.write(myline)
                    outf.write("\n")
        else:
            outf.write(line.rstrip())
            outf.write("\n")


def main():
    '''
    Parse arguments
    '''
    oparser = argparse.ArgumentParser()
    oparser.add_argument("-i", "--input", dest="input", default="-")
    oparser.add_argument("-o", "--output", dest="output", default="-")
    oparser.add_argument(
        "--savelink", dest="savelink", action="store_true", default=False)
    oparser.add_argument(
        "--onlylink", dest="onlylink", action="store_true", default=False)
    opts = oparser.parse_args()

    if opts.input == "-":
        inf = sys.stdin
    else:
        inf = codecs.open(opts.input, "r", "utf8")

    if opts.output == "-":
        outf = sys.stdout
    else:
        outf = codecs.open(opts.output, "w", "utf8")

    operation(inf, outf, opts.savelink, opts.onlylink)


if __name__ == '__main__':
    main()
