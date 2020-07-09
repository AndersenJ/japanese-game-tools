# streaming-tools
Tools for streaming (or just playing) games in Japanese

## OCR Translate
`ocrtranslate.py` is a script that live-translates words in a rectangle on the user's screen. In order for it to work, the following programs must be installed and in the system path:

### Setup
* myougiden (used to fetch dictionary definitions)
* maim
* python3
* pip3
* xdotool
* xinput
* convert (can usually be found in a package labeled imagemagick or something)
* tesseract

You'll also need the japanese data pack for tesseract, and you'll need to install the tinysegmenter3 package through pip3.

### Usage
```
usage: ocrtranslate.py [-h] [-o [O]] [-s [S]]

Uses OCR to live-translate words from Japanese media

optional arguments:
  -h, --help  show this help message and exit
  -o [O]      how many named pipes to send output to
  -s [S]      how many seconds to wait between each output
```

The basic usage is simple. Run `./ocrtranslate.py`. Click on the window you want to translate text from. You will be prompted to click on the top-left corner. This is the top-left corner of the rectangle that will be translated. After you've clicked there, you'll also be prompted to click the bottom-left corner. Once that's done, ocrtranslate.py will start translating the text for you.

Sometimes, you may want to output to multiple terminal windows at a time. In that case, you need to use the `-o` flag. This allows you to specify how many outputs you want to have. For example, `./ocrtranslate -o 4` would output to named pipes `0.pipe`, `1.pipe`, `2.pipe`, and `3.pipe`. You would then use the included `monitorPipe.sh` script to monitor the content of those pipes. In the first terminal window, you would do `./monitorPipe.sh 0.pipe`, and so on. The ocrtranslate.py script will alternate which pipe it outputs to sequentially.

### Troubleshooting
#### The OCR software is doing a poor job of recognizing text.
Try looking at the jp2.png file that gets generated. That's the file that tesseract actually looks at. If that doesn't have sharp text, try tweaking the percentage value in line 204.

#### It isn't recognizing my mouse clicks
Please submit an issue with the output of `xinput --list`. I just need to modify the filter on line 52.

## Deck Generator
`generateDeck.py` is a tool for taking in a body of Japanese text and outputting a .csv document that can be imported into Anki. It takes the most common words in the document which aren't in banlist.list, n4.list, or n5.list, and makes flashcards for them. The flashcards have the target word and the whole line of text it was found on on the front, and the definition on the back.

### Setup
Setup is the same as for OCR Translate, but you don't need maim, tesseract, xdotool, or xinput.

### Usage
`./generateDeck.py gametext.txt gamewords.csv`

You can also add an optional number at the end to specify how many cards you want it to generate. The default is 1000. For example:

`./generateDeck.py gametext.txt gamewords.csv 500`
