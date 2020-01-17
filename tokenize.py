#!/bin/python3

import sys
import tinysegmenter

#statement = "私はアメリカ人"
statement = sys.argv[1]
tokenized_statement = tinysegmenter.tokenize(statement)
print(tokenized_statement)
for token in tokenized_statement:
    print(token)
