#!/usr/bin/env sh

if [ $# -ne 2 ];then
    echo "Usage $0 [input] [output directory]" 2>&1
    exit 1
fi

OUT_DIR=$2
EXTRACTED_DIR=$2/extracted
mkdir -p ${EXTRACTED_DIR}

# Extract
bzcat $1 \
    | sed -e 's/{{仮リンク|\([^|]*\)|[^}]*}}/\1/g' \
          -e 's/{{by|\([^}]*\)}}/\1/g' \
          -e 's/{{日本語版にない記事リンク|\([^|]*\)|[^}]*}}/\1/g'  \
    | WikiExtractor.py --links -c -b 5M -o ${EXTRACTED_DIR} - --quiet \

# Extract
SCRIPT_DIR=$(cd $(dirname $0);pwd)
find ${EXTRACTED_DIR} -type f \
    | xargs bzcat \
    | python3 ${SCRIPT_DIR}/wiki2plain.py --onlylink \
    | python3 ${SCRIPT_DIR}/normalize.py \
    | python3 ${SCRIPT_DIR}/filter.py \
    > ${OUT_DIR}/gold.txt

