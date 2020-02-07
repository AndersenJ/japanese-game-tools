#!/bin/bash

echo "select window with mouse click"
windowid=`xdotool selectwindow`
windowpos=`xdotool getwindowgeometry $windowid | grep -o "[0-9]*,[0-9]*"`
wx=`echo $windowpos | grep -o "^[0-9]*"`
wy=`echo $windowpos | grep -o "[0-9]*$"`
echo $windowpos
echo $wx
echo $wy
sleep 2
MOUSE_ID=$(xinput --list | grep -i -m 1 'mouse\|alps' | grep -o 'id=[0-9]\+' | grep -o '[0-9]\+')
echo $MOUSE_ID

echo "click top-left corner"
STATE1=$(xinput --query-state $MOUSE_ID | grep 'button\[' | sort)
STATE2=$(xinput --query-state $MOUSE_ID | grep 'button\[' | sort)
while [ "$STATE1" == "$STATE2" ]; do
    sleep 0.1
    STATE2=$(xinput --query-state $MOUSE_ID | grep 'button\[' | sort)
done
echo "clicked"
x1=`xdotool getmouselocation | grep -o "x:[0-9]*" | grep -o "[0-9]*"`
y1=`xdotool getmouselocation | grep -o "y:[0-9]*" | grep -o "[0-9]*"`
echo "x1:" $x1
echo "y1:" $y1
sleep 2

echo "click bottom-right corner"
STATE1=$(xinput --query-state $MOUSE_ID | grep 'button\[' | sort)
STATE2=$(xinput --query-state $MOUSE_ID | grep 'button\[' | sort)
while [ "$STATE1" == "$STATE2" ]; do
    sleep 0.1
    STATE2=$(xinput --query-state $MOUSE_ID | grep 'button\[' | sort)
done
echo "clicked"
x2=`xdotool getmouselocation | grep -o "x:[0-9]*" | grep -o "[0-9]*"`
y2=`xdotool getmouselocation | grep -o "y:[0-9]*" | grep -o "[0-9]*"`
echo "x2:" $x2
echo "y2:" $y2
width="$(($x2-$x1))"
height="$(($y2-$y1))"
echo "width: " $width
echo "height: " $height
relx="$(($x1+wx))"
rely="$(($y1+yx))"
geometry="$width"x"$height"+"$x1"+"$y1"
echo $geometry
echo $windowid

while true; do
    maim -g $geometry -q > jp.jpg
    #echo "screenshot captured"

    #time to preprocess the image before letting tesseract at it
    #this works well with hatoful boyfriend
    #convert jp.jpg -black-threshold 98% -negate jp2.jpg

    #this works well with Crosscode
    convert jp.jpg -black-threshold 75% -negate jp2.jpg

    #this works well with Xenoblade Chronicles 2
    #convert jp.jpg -black-threshold 45% -negate jp2.jpg

    #this works well with Celeste
    #convert jp.jpg -black-threshold 60% -negate jp2.jpg

    tesseract jp2.jpg tout -l jpn --dpi 300 2> /dev/null
    echo "text parsed:"
    sed 's/ //g' tout.txt > tout2.txt
    tr -d "\n\r" < tout2.txt > tout3.txt
    cat tout3.txt

    #uncomment to record all captured text
    #cat tout3.txt >> xenoblade.txt

    ./tokenize.py `cat tout3.txt` > tout4.txt
    token=`shuf -n 1 tout4.txt`
    if [ -z "$token" ]
    then
        echo "Text scan unsuccessful"
    else
        echo $token
        myougiden -c --human "$token" | cat
    fi

    sleep 8
done
