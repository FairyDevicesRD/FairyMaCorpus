
# scripts

## Wikipedia Extraction

First, install [WikiExtractor](https://github.com/attardi/wikiextractor).

Then, download wikipedia data and extract texts with a script.
You can get bz2 compressed files and ``gold.txt``.

```sh
wget https://dumps.wikimedia.org/jawiki/latest/jawiki-latest-pages-articles.xml.bz2
./scripts/wiki2txt/dump.sh jawiki-latest-pages-articles.xml.bz2 /path/to/output
```

[Here](https://storage.googleapis.com/fairydevices-public-lang/FairyMaCorpus/jawiki-20170420.gold.txt.xz) is a sample (xz compressed; 99MB; Original:449MB).
It is licensed under [CC-BY-SA 3.0](https://creativecommons.org/licenses/by-sa/3.0/) by [Wikipedia](https://ja.wikipedia.org).

## Error candidate extraction with Wikipedia link
```sh
cat /path/to/output/gold.txt | ./scripts/gold2plain | mecab | gzip  > /path/to/out.mecab.gz

./scripts/eval -g /path/to/output/gold.txt -i <(zcat /path/to/out.mecab.gz) > /path/to/output.json

cat /path/to/output.json | ./scripts/pp > /path/to/output.err.tsv
```

## Filter candidates

```
python3 ./scripts/filter.py \
    -e <(zcat /path/to/excludes.json.gz | jq -r .plain ) \
    -i <(zcat unidic.err.json.gz | python3 ./scripts/pp ) \
    >  /path/to/unidic.only.tsv
```
