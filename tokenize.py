#!/usr/bin/python3

import sys
import tinysegmenter

banlist = set()

#print("Loading banlist")
with open("banlist.list") as ban:
    for word in ban:
        banlist.add(word.strip())

#print("Loading n5 list")
with open("n5.list") as n5:
    for word in n5:
        banlist.add(word.strip())

#print("Loading n4 list")
with open("n4.list") as n4:
    for word in n4:
        banlist.add(word.strip())

tokens = set()


#statement = "私はアメリカ人"
#statement = sys.argv[1]
#print(tokenized_statement)

with open("tout.txt") as lines:
    for line in lines:
        tokenized_statement = tinysegmenter.tokenize(line.strip())
        for token in tokenized_statement:
            if token.strip() not in banlist and token.strip() != "":
                tokens.add(token.strip())

for token in tokens:
    print(token)
