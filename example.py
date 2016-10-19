#! -*- coding: UTF8 -*-
from wordcut import Wordcut
if __name__ == '__main__':
    with open('bigthai.txt') as dict_file:
        word_list = [w.rstrip() for w in dict_file.readlines()]
        word_list.sort()
        wordcut = Wordcut(word_list)
        print(wordcut.tokenize("กากา cat หมา"))
