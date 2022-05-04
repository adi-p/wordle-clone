# Wordle-clone

This program is was written for fun, to play wordle and to explore ways of having a computer play and solve it.

This program is loosely based on [this](https://www.youtube.com/watch?v=v68zYyaEmEA) video by the youtuber 3Blue1Brown.
The code is my own.

## Usage

### For help

`python main.py -h` or `python main.py --help`

```
  usage: main.py [-h] [-p] [-s [{1,2}]] [--sample-word-count SAMPLE_WORD_COUNT]

  optional arguments:
    -h, --help            show this help message and exit
    -p, --play            play Wordle on the command line
    -s [{1,2}], --solve [{1,2}]
                          choose a solver level. Default = 1
    --sample-word-count SAMPLE_WORD_COUNT, -w SAMPLE_WORD_COUNT
                          choose the size of the sample list of words to run the
                          solver with
```
