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


#echo "select window with mouse click"
print("select window with mouse click")
#windowid=`xdotool selectwindow`
windowid = subprocess.check_output(["xdotool", "selectwindow"]).decode("utf-8", "ignore")

#windowpos=`xdotool getwindowgeometry $windowid | grep -o "[0-9]*,[0-9]*"`
xdotool = subprocess.Popen(('xdotool', 'getwindowgeometry', windowid), stdout=subprocess.PIPE)
windowpos = subprocess.check_output(('grep', '-o', '[0-9]*,[0-9]*'), stdin=xdotool.stdout).decode("utf-8", "ignore")
xdotool.wait()

#wx=`echo $windowpos | grep -o "^[0-9]*"`
echo = subprocess.Popen(('echo', windowpos), stdout=subprocess.PIPE)
wx = subprocess.check_output(('grep', '-o', '^[0-9]*'), stdin=echo.stdout).decode("utf-8", "ignore")
echo.wait()
wx = int(wx)

#wy=`echo $windowpos | grep -o "[0-9]*$"`
echo = subprocess.Popen(('echo', windowpos), stdout=subprocess.PIPE)
wy = subprocess.check_output(('grep', '-o', '[0-9]*$'), stdin=echo.stdout).decode("utf-8", "ignore")
echo.wait()
wy = int(wy)

#echo $windowpos
print("windowpos: " + windowpos)
#echo $wx
print("wx: " + str(wx))
#echo $wy
print("wy: " + str(wy))
#sleep 1
time.sleep(1)

#MOUSE_ID=$(xinput --list | grep -i -m 1 'mouse\|alps' | grep -o 'id=[0-9]\+' | grep -o '[0-9]\+')
xinput = subprocess.Popen(('xinput', '--list'), stdout=subprocess.PIPE)
grep1 = subprocess.Popen(('grep', '-i', '-m', '1', 'mouse\|alps'), stdin=xinput.stdout, stdout=subprocess.PIPE)
grep2 = subprocess.Popen(('grep', '-o', 'id=[0-9]\+'), stdin=grep1.stdout, stdout=subprocess.PIPE)
mouseID = subprocess.check_output(('grep', '-o', '[0-9]\+'), stdin=grep2.stdout).decode("utf-8", "ignore")
mouseID = int(mouseID)
grep2.wait()

#echo $MOUSE_ID
print("mouse id: " + str(mouseID))

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

    #x1=`xdotool getmouselocation | grep -o "x:[0-9]*" | grep -o "[0-9]*"`
    xdotool = subprocess.Popen(('xdotool', 'getmouselocation'), stdout=subprocess.PIPE)
    grep = subprocess.Popen(('grep', '-o', 'x:[0-9]*'), stdin=xdotool.stdout, stdout=subprocess.PIPE)
    x1 = subprocess.check_output(('grep', '-o', '[0-9]*'), stdin=grep.stdout).decode("utf-8", "ignore")
    grep.wait()
    x1 = int(x1)

    #y1=`xdotool getmouselocation | grep -o "y:[0-9]*" | grep -o "[0-9]*"`
    xdotool = subprocess.Popen(('xdotool', 'getmouselocation'), stdout=subprocess.PIPE)
    grep = subprocess.Popen(('grep', '-o', 'y:[0-9]*'), stdin=xdotool.stdout, stdout=subprocess.PIPE)
    y1 = subprocess.check_output(('grep', '-o', '[0-9]*'), stdin=grep.stdout).decode("utf-8", "ignore")
    grep.wait()
    y1 = int(y1)
    return x1,y1

#echo "click top-left corner"
print("click top-left corner")
x1, y1 = getMouseLoc(mouseID)

#echo "x1:" $x1
print("x1: " + str(x1))
#echo "y1:" $y1
print("y1: " + str(y1))

#sleep 2
time.sleep(1)

#echo "click bottom-right corner"
print("click bottom-right corner")
x2, y2 = getMouseLoc(mouseID)

#echo "x2:" $x2
print("x2: " + str(x2))
#echo "y2:" $y2
print("y2: " + str(y2))

#width="$(($x2-$x1))"
width = x2 - x1
#height="$(($y2-$y1))"
height = y2 - y1
#echo "width: " $width
print("width: " + str(width))
#echo "height: " $height
print("height: " + str(height))
#relx="$(($x1+wx))"
relx = x1 + wx
#rely="$(($y1+yx))" << ?what is even going on there why did that work?
rely = y1 + wy
#geometry="$width"x"$height"+"$x1"+"$y1"
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
            time.sleep(0.1)
            #print(token + " not found in dictionary")
    return


while 1 == 1:
#    maim -g $geometry -q > jp.jpg
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
    os.system("sed 's/ //g' tout.txt > tout2.txt")
    #tr -d "\n\r" < tout2.txt > tout3.txt
    os.system('cat tout2.txt')

    #uncomment to record all captured text
    #cat tout3.txt >> capture.txt

    printDefs()
