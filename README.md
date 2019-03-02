wordcutpy
=========
wordcutpy is a simple Thai word breaker written in Python 3+

Installation
------------

````
pip install wordcutpy
````


Example
-------

### Conventional verison

````python
#! -*- coding: UTF8 -*-
from wordcut import Wordcut
if __name__ == '__main__':
    with open('bigthai.txt', encoding="UTF-8") as dict_file:
        word_list = list(set([w.rstrip() for w in dict_file.readlines()]))
        wordcut = Wordcut(word_list)
        print(wordcut.tokenize("กากา cat หมา"))
````


### Simplified version


````python
#! -*- coding: UTF8 -*-
from wordcut import Wordcut
wordcut = Wordcut.bigthai()
print(wordcut.tokenize("กากา cat หมา"))
````

Test
----

### Run tests

````shell
python -m unittest discover -s tests
````

