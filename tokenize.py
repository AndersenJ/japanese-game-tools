#!/bin/python3

import tinysegmenter

statement = "私はアメリカ人"
tokenized_statement = tinysegmenter.tokenize(statement)
print(tokenized_statement)
