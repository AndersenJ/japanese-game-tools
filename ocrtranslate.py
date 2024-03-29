#!/usr/bin/python3

import sys
import tinysegmenter
import nagisa
import time
import subprocess
import os
import argparse
from sudachipy import tokenizer
from sudachipy import dictionary
from fugashi import Tagger

fugashi_tagger = Tagger('-Owakati')

sudachipy_tokenizer_obj = dictionary.Dictionary().create()
sudachipy_mode = tokenizer.Tokenizer.SplitMode.C

parser = argparse.ArgumentParser(description='Uses OCR to live-translate words from Japanese media')
parser.add_argument('-o', nargs='?', default=0,
        help='how many named pipes to send output to')
parser.add_argument('-s', nargs='?', default=3,
        help='how many seconds to wait between each output')
args = parser.parse_args()
print(args.o)
seconds = int(args.s)

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
#with open("n4.list") as n4:
#    for word in n4:
#        banlist.add(word.strip())


print("select window with mouse click")
windowid = subprocess.check_output(["xdotool", "selectwindow"]).decode("utf-8", "ignore")

#get the window's position
xdotool = subprocess.Popen(('xdotool', 'getwindowgeometry', windowid), stdout=subprocess.PIPE)
windowpos = subprocess.check_output(('grep', '-o', '[0-9]*,[0-9]*'), stdin=xdotool.stdout).decode("utf-8", "ignore")
xdotool.wait()

echo = subprocess.Popen(('echo', windowpos), stdout=subprocess.PIPE)
wx = subprocess.check_output(('grep', '-o', '^[0-9]*'), stdin=echo.stdout).decode("utf-8", "ignore")
echo.wait()
wx = int(wx)

echo = subprocess.Popen(('echo', windowpos), stdout=subprocess.PIPE)
wy = subprocess.check_output(('grep', '-o', '[0-9]*$'), stdin=echo.stdout).decode("utf-8", "ignore")
echo.wait()
wy = int(wy)

print("windowpos: " + windowpos)
print("wx: " + str(wx))
print("wy: " + str(wy))
time.sleep(1)

#get a valid mouse id. This may not work for some mice.
xinput = subprocess.Popen(('xinput', '--list'), stdout=subprocess.PIPE)
grep0 = subprocess.Popen(('grep', '-v', 'ergosaurus'), stdin=xinput.stdout, stdout=subprocess.PIPE)
grep1 = subprocess.Popen(('grep', '-i', '-m', '1', 'mouse\|alps\|logitech'), stdin=grep0.stdout, stdout=subprocess.PIPE)
grep2 = subprocess.Popen(('grep', '-o', 'id=[0-9]\+'), stdin=grep1.stdout, stdout=subprocess.PIPE)
mouseID = subprocess.check_output(('grep', '-o', '[0-9]\+'), stdin=grep2.stdout).decode("utf-8", "ignore")
mouseID = int(mouseID)
grep2.wait()

print("mouse id: " + str(mouseID))

#gets the current x/y coordinates of the mouse
def getMouseLoc(mouseID):
    xinput = subprocess.Popen(('xinput', '--query-state', str(mouseID)), stdout=subprocess.PIPE)
    grep = subprocess.Popen(('grep', 'button\['), stdin=xinput.stdout, stdout=subprocess.PIPE)
    state1 = subprocess.check_output(('sort'), stdin=grep.stdout).decode("utf-8", "ignore")
    grep.wait()

    state2 = state1

    while state1 == state2:
        time.sleep(0.1)

        xinput = subprocess.Popen(('xinput', '--query-state', str(mouseID)), stdout=subprocess.PIPE)
        grep = subprocess.Popen(('grep', 'button\['), stdin=xinput.stdout, stdout=subprocess.PIPE)
        state1 = subprocess.check_output(('sort'), stdin=grep.stdout).decode("utf-8", "ignore")
        grep.wait()

    print("clicked")

    xdotool = subprocess.Popen(('xdotool', 'getmouselocation'), stdout=subprocess.PIPE)
    grep = subprocess.Popen(('grep', '-o', 'x:[0-9]*'), stdin=xdotool.stdout, stdout=subprocess.PIPE)
    x = subprocess.check_output(('grep', '-o', '[0-9]*'), stdin=grep.stdout).decode("utf-8", "ignore")
    grep.wait()
    x = int(x)

    xdotool = subprocess.Popen(('xdotool', 'getmouselocation'), stdout=subprocess.PIPE)
    grep = subprocess.Popen(('grep', '-o', 'y:[0-9]*'), stdin=xdotool.stdout, stdout=subprocess.PIPE)
    y = subprocess.check_output(('grep', '-o', '[0-9]*'), stdin=grep.stdout).decode("utf-8", "ignore")
    grep.wait()
    y = int(y)
    return x,y

print("click top-left corner")
x1, y1 = getMouseLoc(mouseID)

print("x1: " + str(x1))
print("y1: " + str(y1))

time.sleep(1)

print("click bottom-right corner")
x2, y2 = getMouseLoc(mouseID)

print("x2: " + str(x2))
print("y2: " + str(y2))

width = x2 - x1
height = y2 - y1
print("width: " + str(width))
print("height: " + str(height))
relx = x1 + wx
#rely="$(($y1+yx))" << ?what is even going on there why did that work?
rely = y1 + wy
geometry = str(width) + "x" + str(height) + "+" + str(x1) + "+" + str(y1)
print(geometry)
print(windowid)

def printDefs(outputs, seconds):
    if not hasattr(printDefs, "counter"):
        printDefs.counter = 0
    if not hasattr(printDefs, "tokenization_counter"):
        printDefs.tokenization_counter = 0
    tokens = set()
    with open("tout3.txt") as lines:
        for line in lines:
            if printDefs.tokenization_counter % 3 == 0:
                tinysegmenter_tokens = tinysegmenter.tokenize(line.strip())
                print("tinysegmenter:")
                tokenized_statement = tinysegmenter_tokens
            elif printDefs.tokenization_counter % 3 == 1:
                nagisa_tokens = nagisa.tagging(line.strip()).words
                print("nagisa:")
                tokenized_statement = nagisa_tokens
            elif printDefs.tokenization_counter % 3 == 2:
                print("fugashi (MeCab):")
                tokenized_statement = [word.surface for word in fugashi_tagger(line.strip())]
            else:
                print("sudachipy:")
                tokenized_statement = [m.surface() for m in sudachipy_tokenizer_obj.tokenize(line.strip(), sudachipy_mode)]
            print(tokenized_statement)
            printDefs.tokenization_counter += 1
            for token in tokenized_statement:
                t = token.strip()
                t = sudachipy_tokenizer_obj.tokenize(t, sudachipy_mode)[0].dictionary_form()
                if t not in banlist and t != "":
                    tokens.add(t)

    if len(tokens) == 0:
        time.sleep(1)
    translated = []
    for token in tokens:
        try:
            definition = subprocess.check_output(["myougiden", "-f", "--human", "-c", "-e", "whole", token.replace("|","!")]).decode("utf-8", "ignore")
            if len(outputs) == 0:
                print("")
                print("----------------------------------------------------------------------")
                print("")
                print(token)
                print(definition)
            else:
                print("outputting " + token + " to " + outputs[printDefs.counter % len(outputs)])
                f = open(outputs[printDefs.counter % len(outputs)], "a")
                f.write("\n\n\n---------------------------------------------\n\n\n\n")
                f.write(token)
                f.write("\n")
                f.write(definition)
                f.close()
                printDefs.counter += 1
            time.sleep(seconds)
        except:
            try:
                definition = subprocess.check_output(["myougiden", "--human", "-c", "-e", "whole", token.replace("|","!")]).decode("utf-8", "ignore")
                if len(outputs) == 0:
                    print("")
                    print("----------------------------------------------------------------------")
                    print("")
                    print(token)
                    print(definition)
                else:
                    print("outputting " + token + " to " + outputs[printDefs.counter % len(outputs)])
                    f = open(outputs[printDefs.counter % len(outputs)], "a")
                    f.write("\n\n\n---------------------------------------------\n\n\n\n")
                    f.write(token)
                    f.write("\n")
                    f.write(definition)
                    f.close()
                    printDefs.counter += 1
                time.sleep(seconds)
            except:
                time.sleep(0.01)
            #print(token + " not found in dictionary")
    return

numOutputs = int(args.o)
outputs = []
if numOutputs > 0:
    for i in range(numOutputs):
        os.system('mkfifo ' + str(i) + '.pipe')
        #f = open(str(i) + '.pipe', 'a')
        #outputs.append(f)
        outputs.append(str(i) + '.pipe')


while 1 == 1:
    os.system('maim -g ' + geometry + ' -q > jp.jpg')
    print("screenshot captured")

    #time to preprocess the image before letting tesseract at it
    #this works well with hatoful boyfriend
    #convert jp.jpg -black-threshold 98% -negate jp2.jpg

    #this works well with Crosscode
    #os.system('convert jp.jpg -black-threshold 75% -negate jp2.jpg')

    #this works well with Valkyria Chronicles 4
    #os.system('convert jp.jpg -black-threshold 44% -negate jp2.jpg')

    #tokyo xanadu
    #os.system('convert jp.jpg -black-threshold 60% -negate jp2.jpg')

    #Pokemon SwSh
    #os.system('convert jp.jpg -black-threshold 60% jp2.jpg')

    #Baten Kaitos
    #os.system('convert jp.jpg -black-threshold 35% jp2.jpg')
    #os.system('convert jp2.jpg -white-threshold 35% jp3.jpg')
    os.system('convert jp.jpg -threshold 39% jp2.jpg')

    #this works well with Xenoblade Chronicles 2
    #convert jp.jpg -black-threshold 45% -negate jp2.jpg

    #this works well with Celeste
    #convert jp.jpg -black-threshold 60% -negate jp2.jpg

    os.system('tesseract jp2.jpg tout -l jpn --dpi 300')
    print("text parsed:")
    #could probably get rid of this sed call later with a simple .replace
    #it's only there in the first place because tesseract inserts
    #spaces between the characters where there should be none
    os.system("sed 's/ //g' tout.txt > tout2.txt")
    os.system('tr -d "\n\r" < tout2.txt > tout3.txt')
    os.system('cat tout3.txt')

    #uncomment to record all captured text
    #os.system('cat tout2.txt >> capture.txt')

    printDefs(outputs, seconds)
