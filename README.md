wordcutpy
=========
wordcutpy is a simple Thai word breaker written in Python

Example
-------
```python
#! -*- coding: UTF8 -*-
from wordcut import Wordcut
if __name__ == '__main__':
    wordcut = Wordcut(map(lambda w: w.rstrip().decode("UTF-8"), 
                          open('dict.txt').readlines()))
    print u"|".join(wordcut.tokenize(u"กากา cat หมา"))
```
