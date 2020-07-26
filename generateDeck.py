#!/bin/python3

import sys
import codecs
import tinysegmenter
import nagisa
import subprocess

n4words = set()
n5words = set()
banlist = set()

print("Loading banlist")
with open("banlist.list") as ban:
    for word in ban:
        banlist.add(word.strip())

print("Loading n5 list")
with open("n5.list") as n5:
    for word in n5:
        n5words.add(word.strip())

print("Loading n4 list")
with open("n4.list") as n4:
    for word in n4:
        n4words.add(word.strip())

occurrences = {}
sentences = {}

print("Counting words")
with codecs.open(sys.argv[1], 'r', encoding='utf-8', errors='ignore') as infile:
    for line in infile:
        #print(line)
        tokenizedLine = tinysegmenter.tokenize(line.strip()) + nagisa.tagging(line.strip()).words
        for token in tokenizedLine:
            if token not in banlist and token not in n5words and token not in n4words and token.strip() != "":
                if token in occurrences.keys():
                    occurrences[token] += 1
                else:
                    occurrences[token] = 1
                if token not in sentences.keys():
                    sentences[token] = line.replace("\n", "").replace("|","!")

print("Sorting words")
sortedOccurrences = []
for character in occurrences.keys():
    sortedOccurrences.append([
                character,
                occurrences[character]
            ])

sortedOccurrences = sorted(sortedOccurrences, key=lambda occurrence: -occurrence[1])

maxCount = 1000
try:
    maxCount = int(sys.argv[3])
except:
    maxCount = 1000

count = 0
outfile = open(sys.argv[2], 'w')
print("Loading definitions and writing to " + sys.argv[2])
for character in sortedOccurrences:
    if count >= maxCount:
        break
    print(str(count) + "/" + str(len(sortedOccurrences)) + "	" + character[0])
    try:
        definition = subprocess.check_output(["myougiden", "-f", "--human", "-e", "whole", character[0].replace("|","!")]).decode("utf-8", "ignore").replace("\n", "<br>")
        outfile.write(character[0] + "<br>" + sentences[character[0]] + "|" + str(character[1]) + "|" + definition + "|\n")
        count += 1
    except:
        try:
            definition = subprocess.check_output(["myougiden", "--human", "-e", "whole", character[0].replace("|","!")]).decode("utf-8", "ignore").replace("\n", "<br>")
            outfile.write(character[0] + "<br>" + sentences[character[0]] + "|" + str(character[1]) + "|" + definition + "|\n")
            count += 1
        except:
            definition = "error"
            print("error processing " + character[0])
            print("skipping " + character[0])
outfile.close()
