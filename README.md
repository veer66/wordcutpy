wordcutpy
=========
wordcutpy is a simple Thai word breaker written in Python 3+

Example
-------
````python
#! -*- coding: UTF8 -*-
from wordcut import Wordcut
if __name__ == '__main__':
    with open('bigthai.txt', encoding="UTF-8") as dict_file:
        word_list = list(set([w.rstrip() for w in dict_file.readlines()]))
        wordcut = Wordcut(word_list)
        print(wordcut.tokenize("กากา cat หมา"))
````
