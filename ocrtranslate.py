#!/usr/bin/python3

import sys
import tinysegmenter
import time
import subprocess
import os

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
grep1 = subprocess.Popen(('grep', '-i', '-m', '1', 'mouse\|alps'), stdin=xinput.stdout, stdout=subprocess.PIPE)
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

def printDefs():
    tokens = set()
    with open("tout2.txt") as lines:
        for line in lines:
            tokenized_statement = tinysegmenter.tokenize(line.strip())
            for token in tokenized_statement:
                t = token.strip()
                if t not in banlist and t != "":
                    tokens.add(t)

    translated = []
    for token in tokens:
        try:
            definition = subprocess.check_output(["myougiden", "--human", "-c", "-e", "whole", token.replace("|","!")]).decode("utf-8", "ignore")
            print("")
            print("----------------------------------------------------------------------------")
            print("")
            print(token)
            print(definition)
            time.sleep(4)
        except:
            time.sleep(0.01)
            #print(token + " not found in dictionary")
    return


while 1 == 1:
    os.system('maim -g ' + geometry + ' -q > jp.jpg')
    print("screenshot captured")

    #time to preprocess the image before letting tesseract at it
    #this works well with hatoful boyfriend
    #convert jp.jpg -black-threshold 98% -negate jp2.jpg

    #this works well with Crosscode
    os.system('convert jp.jpg -black-threshold 75% -negate jp2.jpg')

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
    os.system('cat tout2.txt')

    #uncomment to record all captured text
    #os.system('cat tout2.txt >> capture.txt')

    printDefs()
