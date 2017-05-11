#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Stub
'''

import argparse
import codecs
import sys


def operation(inf, exf, outf):
    '''
    Stub
    '''
    excludes = set([])
    for line in exf:
        key = line[:-1].replace("|", "").replace("?", "")
        excludes.add(key)

    for line in inf:
        sep = line.find("\t")
        key = line[:sep].replace("|", "").replace("?", "")
        if key not in excludes:
            outf.write(line)


def main():
    '''
    Parse arguments
    '''
    oparser = argparse.ArgumentParser()
    oparser.add_argument("-i", "--input", dest="input", default="-")
    oparser.add_argument("-e", "--exclude", dest="exclude", default="-")
    oparser.add_argument("-o", "--output", dest="output", default="-")
    oparser.add_argument(
        "--verbose", dest="verbose", action="store_true", default=False)
    opts = oparser.parse_args()

    if opts.input == "-":
        inf = sys.stdin
    else:
        inf = codecs.open(opts.input, "r", "utf8")

    if opts.exclude == "-":
        exf = sys.stdin
    else:
        exf = codecs.open(opts.exclude, "r", "utf8")

    if opts.output == "-":
        outf = sys.stdout
    else:
        outf = codecs.open(opts.output, "w", "utf8")
    operation(inf, exf, outf)


if __name__ == '__main__':
    main()
