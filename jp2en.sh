#!/bin/bash

maim -b 0 --select -q > jp.png
tesseract jp.png tout -l jpn 2> /dev/null
sed 's/ //g' tout.txt > tout2.txt
cat tout2.txt
#trans -brief "`cat tout2.txt`"
#sleep 1
#trans -s 日本語 --show-original n "`cat tout2.txt`"
trans -s 日本語 -brief --show-original Y -i tout2.txt
sleep 2
rm tout.txt tout2.txt jp.png
