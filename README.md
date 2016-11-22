# █ Blackout █

For [NaNoGenMo 2016](https://github.com/NaNoGenMo/2016).

_Blackout_ generates pages of text from book or newspaper scans in the style of [Newspaper Blackout Poetry](http://newspaperblackout.com/), popularized by [Austin Kleon](https://twitter.com/austinkleon) (related to work like [A Humument](http://tomphillipshumument.tumblr.com/) by Tom Phillips).

_Blackout_ does the following:

1. Take, as input, an image of text, from a newspaper or book.
2. Run [OCR](https://github.com/jflesch/pyocr) against the image, identifying the words and their bounding boxes.
3. Feed the extracted text into a [natural language parser](https://spacy.io/), categorizing each part of speech.
3. Given one of many randomly selected [Tracery](https://github.com/aparrish/pytracery) grammars, select words from the current page that match the parts of speech of that grammar.
4. Draw around those words and "scribble" out all other text on the page image.
5. Output the final page as a new image.

Pen width, line length, line direction, number of strokes, and stroke opacity are all randomly fuzzed. The pen color is always black, except in rare cases it is blood red.

_Blackout_ has produced one creative work:

## "The Days Left Forebodings and Water"

<img src="https://github.com/lizadaly/blackout/blob/master/images/title.png?raw=true" />

The source material is [A Vindication of the Rights of Women](https://en.wikipedia.org/wiki/A_Vindication_of_the_Rights_of_Woman) by Mary Wollstonecraft.

Read [The Days Left Forebodings and Water](https://s3.amazonaws.com/worldwritable/nanogenmo2016-short.pdf). 45 pages long, consists of entries that were generated randomly, but hand-picked and ordered.



<img src="https://github.com/lizadaly/blackout/blob/master/images/1.png?raw=true" />

<img src="https://github.com/lizadaly/blackout/blob/master/images/2.png?raw=true" />

<img src="https://github.com/lizadaly/blackout/blob/master/images/3.png?raw=true" />

<img src="https://github.com/lizadaly/blackout/blob/master/images/4.png?raw=true" />

<img src="https://github.com/lizadaly/blackout/blob/master/images/6.png?raw=true" />

<img src="https://github.com/lizadaly/blackout/blob/master/images/7.png?raw=true" />


(The full NaNoGenMo entry of ~50,000 words is a [9.3GB PDF](https://s3.amazonaws.com/worldwritable/nanogenmo2016-9g-long.pdf) of nearly 10,000 pages. *You almost certainly do not want to download it.*)
