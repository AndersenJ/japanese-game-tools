#!/bin/python3

import argparse
import sys

parser = argparse.ArgumentParser(description='Generates csv files from bodies of Japanese text for use with Anki')
parser.add_argument('japanese_text_file')
parser.add_argument('output_file')
parser.add_argument('-w', nargs='?', default="1000",
        help='how many words to put in the output csv')
parser.add_argument('-m', action='store_true',
        help='indications that in addition to the words, the user wishes to memorize the entire input file line-by-line; useful for songs')
args = parser.parse_args()
print("Input file: " + args.japanese_text_file)
print("Output file: " + args.output_file)
print("Number of words to make cards for: " + args.w)
print(args.m)

import codecs
import tinysegmenter
import nagisa
import subprocess
from sudachipy import tokenizer
from sudachipy import dictionary


maxCount = int(args.w)

sudachipy_tokenizer_obj = dictionary.Dictionary().create()
sudachipy_mode = tokenizer.Tokenizer.SplitMode.C

japanesequest1000 = set()
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

print("Loading JapaneseQuest list")
with open("japanesequest1000.mylist") as jq:
    for word in jq:
        japanesequest1000.add(word.strip())

occurrences = {}
sentences = {}

print("Counting words")
linenum = 0
lines = []
lines.append("begin")

segmenter = tinysegmenter.TinySegmenter()
with codecs.open(args.japanese_text_file, 'r', encoding='utf-8', errors='ignore') as infile:
    for line in infile:
        lines.append(line.strip())
        linenum += 1
        #print(line)
        print("tokenizing")
        tokenizedLine = segmenter.tokenize(line.strip()) + nagisa.tagging(line.strip()).words
        print("tokenized")
        for token in tokenizedLine:
            token = sudachipy_tokenizer_obj.tokenize(token, sudachipy_mode)[0].dictionary_form()
            if token not in banlist and token not in n5words and token not in n4words and token not in japanesequest1000 and token.strip() != "":
                if token in occurrences.keys():
                    occurrences[token] += 1
                else:
                    occurrences[token] = 1
                if token not in sentences.keys():
                    sentences[token] = line.replace("\n", "").replace("|","!")
        if linenum % 100 == 0:
            print("finished counting words from " + str(linenum) + " lines")

print("Sorting words")
sortedOccurrences = []
for character in occurrences.keys():
    sortedOccurrences.append([
                character,
                occurrences[character]
            ])

sortedOccurrences = sorted(sortedOccurrences, key=lambda occurrence: -occurrence[1])

count = 0
outfile = open(args.output_file, 'w')
print("Loading definitions and writing to " + args.output_file)
for character in sortedOccurrences:
    if count >= maxCount:
        break
    print(str(count) + "/" + str(len(sortedOccurrences)) + "	" + character[0])
    try:
        definition = subprocess.check_output(["myougiden", "-f", "--human", "-e", "whole", character[0].replace("|","!")]).decode("utf-8", "ignore").replace("\n", "<br>")
        #outfile.write(character[0] + "<br>" + sentences[character[0]] + "|" + str(character[1]) + "|" + definition + "\n")
        outfile.write(character[0] + "|" + str(character[1]) + "|" + definition + "<br>" + sentences[character[0]] + "\n")
        count += 1
    except:
        try:
            definition = subprocess.check_output(["myougiden", "--human", "-e", "whole", character[0].replace("|","!")]).decode("utf-8", "ignore").replace("\n", "<br>")
            #outfile.write(character[0] + "<br>" + sentences[character[0]] + "|" + str(character[1]) + "|" + definition + "\n")
            outfile.write(character[0] + "|" + str(character[1]) + "|" + definition + "<br>" + sentences[character[0]] + "\n")
            count += 1
        except:
            definition = "error"
            print("error processing " + character[0])
            print("skipping " + character[0])

if args.m:
    lines.append("end")
    for i in range(1, len(lines)-1):
        outfile.write(lines[i-1] + "<br>")
        for j in range(len(lines[i])):
            outfile.write("ー")
        outfile.write("<br>" + lines[i+1] + "|-1|")
        outfile.write(lines[i-1] + "<br>")
        outfile.write(lines[i])
        outfile.write("<br>" + lines[i+1] + "\n")
outfile.close()
