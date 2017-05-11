

# Fairy Morphological Annotated Corpus

[![CircleCI](https://circleci.com/gh/FairyDevicesRD/FairyMaCorpus.svg?style=svg)](https://circleci.com/gh/FairyDevicesRD/FairyMaCorpus)
[![Apache License](http://img.shields.io/badge/license-APACHE2-blue.svg)](http://www.apache.org/licenses/LICENSE-2.0)

This corpus includes morphological partial annotations for Japanese Wikipedia.
The main purpose is more like error check for morphological analyzers than their training.
This is a sample data.

```
また、銀河系にある|いて?座?Ａ?＊|のブラックホールの４００倍も重い。
(Furthermore, it is also 400 times heavier than the black hole of Sagittarius A * in the galaxy.)
```

``|`` indicates word boundary.
``?`` between first and last ``|`` indicate word boundary candidates.

This corpus reveals some morphological analyzers wrongly parse it as ``あるい|て`` (あるい(walk) and て(and)).


## Files

- corpus
    - First column in each ``.tsv`` file includes annotated texts.
    - Other columns contain additional information.
- scripts
   - See [README](scripts/README.md)


## References

```bib
@INPROCEEDINGS{hayashibe:2017:SIGNL231,
    author    = {林部祐太},
    title     = {日本語部分形態素アノテーションコーパスの構築},
    booktitle = "情報処理学会第231回自然言語処理研究会",
    year      = "2017",
    pages     = "NL-231-9:1-8",
    publisher = "情報処理学会",
}
```


## License

- Corpus
    - Wikipedia: ``corpus/wikipedia``
        - Original [Wikipedia](https://ja.wikipedia.org) texts are licensed under [CC-BY-SA 3.0](https://creativecommons.org/licenses/by-sa/3.0/) and available at [Dump site](https://dumps.wikimedia.org/jawiki/)
        - Additional annotation information is licensed under [Apache License 2.0](http://www.apache.org/licenses/LICENSE-2.0) by [Fairy Devices Inc](http://www.fairydevices.jp/)
    - Original: ``corpus/original``
        - Licensed under [Apache License 2.0](http://www.apache.org/licenses/LICENSE-2.0) by [Fairy Devices Inc](http://www.fairydevices.jp/)
- Scripts: ``scripts``
    - Licensed under [Apache License 2.0](http://www.apache.org/licenses/LICENSE-2.0) by [Fairy Devices Inc](http://www.fairydevices.jp/)

