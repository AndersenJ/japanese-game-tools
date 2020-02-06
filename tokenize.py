#!/bin/python3

import sys
import tinysegmenter

#statement = "私はアメリカ人"
statement = sys.argv[1]
tokenized_statement = tinysegmenter.tokenize(statement)
#print(tokenized_statement)

banlist = ["", " ", "は", "の", "で", "だっ", "する", "、", "", "。", "て", "が", "に", "お", "と"]

for token in tokenized_statement:
    if token not in banlist:
        print(token)
