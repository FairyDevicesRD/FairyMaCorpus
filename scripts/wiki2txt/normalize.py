#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# https://github.com/neologd/mecab-ipadic-neologd/wiki/Regexp.ja
import re
import unicodedata
import argparse
import sys


def remove_extra_spaces(s):
    s = re.sub('[ 　]+', '　', s)
    blocks = ''.join(('\u4E00-\u9FFF',  # CJK UNIFIED IDEOGRAPHS
                      '\u3040-\u309F',  # HIRAGANA
                      '\u30A0-\u30FF',  # KATAKANA
                      '\u3000-\u303F',  # CJK SYMBOLS AND PUNCTUATION
                      '\uFF00-\uFF0F',
                      '\uFF5B-\uFFEF',
                      # HALFWIDTH AND FULLWIDTH FORMS
                      #                       '\uFF00-\uFFEF'   # HALFWIDTH AND FULLWIDTH FORMS
                      ))
    basic_latin = '\uFF01-\uFF5E'

    def remove_space_between(cls1, cls2, s):
        p = re.compile('([{}])　([{}])'.format(cls1, cls2))
        while p.search(s):
            s = p.sub(r'\1\2', s)
        return s

    s = remove_space_between(blocks, blocks, s)
    s = remove_space_between(blocks, basic_latin, s)
    s = remove_space_between(basic_latin, blocks, s)
    return s


def normalize(s):
    s = s.strip()
    s = unicodedata.normalize('NFKC', s)

    def maketrans(f, t):
        return {ord(x): ord(y) for x, y in zip(f, t)}
    transdic = maketrans('!"#$%&\'()*+,./:;<=>?@[¥]^_`{|}~｡､･｢｣',
                         '！”＃＄％＆’（）＊＋，．／：；＜＝＞？＠［￥］＾＿｀｛｜｝〜。、・「」')

    def add_transdic(transdic, from_char, to_char, base):
        for idx, orig in enumerate(range(ord(from_char), ord(to_char) + 1)):
            transdic[orig] = ord(base) + idx

    add_transdic(transdic, '0', '9', '０')
    add_transdic(transdic, 'A', 'Z', 'Ａ')
    add_transdic(transdic, 'a', 'z', 'ａ')

#         '｡-ﾟ'
#         '｡-ﾟ'

    s = s.translate(transdic)
    s = re.sub('[\u002D\u2010\u2043\u02D7\u2212\u29FF\u2796\u207B\u208B]+', '\uFF0D', s)  # normalize hyphens to  U+2015
    s = re.sub('[\u30FC]+', '\u30FC', s)  # normalize choonpus to  U+30FC
    s = re.sub('[~∼∾〜〰～]', '', s)  # remove tildes
    s = remove_extra_spaces(s)
    return s



def test():
    assert "０１２３４５６７８９" == normalize("0123456789")
    assert "０１２３４５６７８９" == normalize("０１２３４５６７８９")
    assert "ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ" == normalize("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    assert "ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ" == normalize("ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ")
    assert "ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚ" == normalize("abcdefghijklmnopqrstuvwxyz")
    assert "！”＃＄％＆’（）＊＋，．／：；＜＞？＠［￥］＾＿｀｛｜｝" == normalize("!\"#$%&'()*+,./:;<>?@[¥]^_`{|}")
    assert "＝。、・「」" == normalize("＝。、・「」")
    assert '。「」、・' == normalize('｡｢｣､･')
    assert "ハンカク" == normalize("ﾊﾝｶｸ")
    assert "ｏ\uFF0Dｏ" == normalize("o₋o")
    assert "わい" == normalize("わ〰い")
    assert "スーパー" == normalize("スーパーーーー")
    assert "！＃" == normalize("!#")
    assert "ゼンカクスペース" == normalize("ゼンカク　スペース")
    assert "おお" == normalize("お             お")
    assert "おお" == normalize("      おお")
    assert "おお" == normalize("おお      ")
    assert "検索エンジン自作入門を買いました！！！" == \
        normalize("検索 エンジン 自作 入門 を 買い ました!!!")
    assert "アルゴリズムＣ" == normalize("アルゴリズム C")
    assert "ＰＲＭＬ副読本" == normalize("　　　ＰＲＭＬ　　副　読　本　　　")
    assert "Ｃｏｄｉｎｇ　ｔｈｅ　Ｍａｔｒｉｘ" == normalize("Coding the Matrix")
    assert "南アルプスの天然水Ｓｐａｒｋｉｎｇ　Ｌｅｍｏｎレモン一絞り" == \
        normalize("南アルプスの　天然水　Sparking Lemon　レモン一絞り")
    sys.stderr.write("Test passed.\n")

if __name__ == "__main__":
    oparser = argparse.ArgumentParser()
    oparser.add_argument("--test", dest="test", action="store_true", default=False)
    opts = oparser.parse_args()

    if opts.test:
        test()
    else:
        for line in sys.stdin:
            sys.stdout.write(normalize(line))
            sys.stdout.write("\n")
