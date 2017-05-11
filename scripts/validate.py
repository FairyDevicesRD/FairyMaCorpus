#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Stub
'''

import argparse
import codecs
import sys


def operation(inf, outf):
    '''
    Check
    '''
    err = False
    annotations = set([])
    for line in inf:
        if line.startswith(";"):
            continue

        items = line[:-1].split("\t")
        if len(items) == 0:
            continue

        # Only | and ? are allowed to use in ASCII characters.
        annotation = items[0]
        for char in annotation:
            if ord(char) <= 128:
                if char not in ['|', '?']:
                    outf.write("Illigal ASCII character: %s (%s)\n" % (char, ord(char)))
                    err = True
        if annotation in annotations:
            outf.write("Duplication: %s\n" % (annotation))
            err = True
        annotations.add(annotation)
    return err


def main():
    '''
    Parse arguments
    '''
    oparser = argparse.ArgumentParser()
    oparser.add_argument("-i", "--input", dest="input", default="-")
    oparser.add_argument("-o", "--output", dest="output", default="-")
    oparser.add_argument(
        "--verbose", dest="verbose", action="store_true", default=False)
    opts = oparser.parse_args()

    if opts.input == "-":
        inf = sys.stdin
    else:
        inf = codecs.open(opts.input, "r", "utf8")

    if opts.output == "-":
        outf = sys.stdout
    else:
        outf = codecs.open(opts.output, "w", "utf8")
    err = operation(inf, outf)
    if err:
        sys.exit(-1)


if __name__ == '__main__':
    main()
