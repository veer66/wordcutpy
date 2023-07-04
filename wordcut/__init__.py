"""wordcutpy is a word tokenizer written in Python."""

import re


class PrefixTree:
    """PrefixTree is a hash tree for storing and searching word list."""

    def __init__(self, members_with_payload):
        """Prefix tree is constructed from sorted members with payload."""
        self.tab = {}
        if members_with_payload is None:
            return None
        sorted_members_with_payload = sorted(members_with_payload,
                                             key=lambda i: i[0])

        for i in range(len(sorted_members_with_payload)):
            members, payload = sorted_members_with_payload[i]
            row_no = 0
            for j in range(len(members)):
                is_terminal = len(members) == j + 1
                member = members[j]
                key = (row_no, j, member)
                if key in self.tab:
                    row_no = self.tab[key][0]
                else:
                    val = (i, is_terminal, payload if is_terminal else None)
                    self.tab[key] = val
                    row_no = i

    def lookup(self, i, offset, member):
        """Lookup is done by searching an element of members in the tree."""
        key = (i, offset, member)
        if key not in self.tab:
            return None
        return self.tab[key]


UNK = 1
DICT = 2
INIT = 3
LATIN = 4
PUNC = 5


def is_better(link0, link1):
    """Links are compared by their properies."""
    if link0 is None:
        return True

    if link1["unk"] < link0["unk"]:
        return True

    if link1["w"] < link0["w"]:
        return True

    return False


class LatinTransducer:
    """Latin transducer detects latin tokens."""

    def __init__(self):
        """Latin transducer is constructed by letting pointers to be None."""
        self.latin_s = None
        self.latin_e = None

    def update(self, ch, i, s):
        """Update by feeding a character, its position, and the string."""
        if self.latin_s is None:
            if re.match("[A-Za-z]", ch):
                self.latin_s = i
        else:
            if re.match("[A-Za-z]", ch):
                if i + 1 == len(s) or not re.match("[A-Za-z]", s[i + 1]):
                    self.latin_e = i + 1
            else:
                self.latin_s = None
                self.latin_e = None

    def create_link(self, path):
        """Pointers are used for creating a link."""
        if self.latin_s is not None and self.latin_e is not None:
            p_link = path[self.latin_s]
            _link = {"p": self.latin_s,
                     "w": p_link["w"] + 1,
                     "unk": p_link["unk"],
                     "type": LATIN}
            return _link
        return None


class PuncTransducer:
    """Punc Transducer detects puncuation tokens."""

    def __init__(self):
        """Punc Transducer is constructed by letting pointers to be None."""
        self.punc_s = None
        self.punc_e = None

    def update(self, ch, i, s):
        """Update by feeding a character, its position, and the string."""
        if self.punc_s is None:
            if ch == " ":
                self.punc_s = i
        else:
            if ch == " ":
                if len(s) == i + 1 or s[i + 1] != " ":
                    self.punc_e = i + 1
            else:
                self.punc_s = None
                self.punc_e = None

    def create_link(self, path):
        """Pointers are used for creating a link."""
        if self.punc_s is not None and self.punc_e is not None:
            p_link = path[self.punc_s]
            _link = {"p": self.punc_s,
                     "w": p_link["w"] + 1,
                     "unk": p_link["unk"],
                     "type": PUNC}
            return _link
        return None


def build_path(dix, s):
    """Build path constructs word tokenization path."""
    left_boundary = 0
    dict_acc_list = []

    path = [{"p": None, "w": 0, "unk": 0, "type": INIT}]

    punc_transducer = PuncTransducer()
    latin_transducer = LatinTransducer()

    for i, ch in enumerate(s):
        dict_acc_list.append({"s": i, "p": 0, "final": False})

        # Update dict acceptors
        _dict_acc_list = dict_acc_list
        dict_acc_list = []
        for acc in _dict_acc_list:
            offset = i - acc["s"]
            child = dix.lookup(acc["p"], offset, ch)
            if child is not None:
                child_p, is_final, payload = child
                dict_acc_list.append({"s": acc["s"], "p": child_p,
                                      "final": is_final})
        latin_transducer.update(ch, i, s)
        punc_transducer.update(ch, i, s)

        # select link
        link = None

        # links from wordlist
        for acc in dict_acc_list:
            if acc["final"]:
                p_link = path[acc["s"]]
                _link = {"p": acc["s"],
                         "w": p_link["w"] + 1,
                         "unk": p_link["unk"],
                         "type": DICT}
                if is_better(link, _link):
                    link = _link

        _link = latin_transducer.create_link(path)
        if _link is not None and is_better(link, _link):
            link = _link

        _link = punc_transducer.create_link(path)
        if _link is not None and is_better(link, _link):
            link = _link

        # fallback
        if link is None:
            p_link = path[left_boundary]
            link = {"p": left_boundary,
                    "w": p_link["w"] + 1,
                    "unk": p_link["unk"] + 1,
                    "type": UNK}

        path.append(link)

        if link["type"] != UNK:
            if link["type"] == LATIN or link["type"] == PUNC:
                left_boundary = i + 1
            else:
                left_boundary = i

    return path


def path_to_tokens(txt, path):
    """Path to Token transforms a path to a list of tokens."""
    if len(path) < 2:
        return None

    e = len(path) - 1
    toks = []

    while True:
        link = path[e]
        s = link["p"]
        if s is None:
            break
        toks.append(txt[s:e])
        e = s

    toks.reverse()
    return toks


def tokenize(dix, txt):
    """Tokenize splits a string to a list of tokens."""
    if txt is None or txt == "":
        return []
    path = build_path(dix, txt)
    return path_to_tokens(txt, path)


class Wordcut:
    """Wordcut wraps functions and data related tokenizaion."""

    def __init__(self, wordlist):
        """Wordcut is constructed by a sorted list of words."""
        self.dix = PrefixTree([(word, None) for word in wordlist])

    @classmethod
    def bigthai(cls):
        """Bigthai constructs Wordcut based on a big Thai word list."""
        import os
        "Initialize from bigthai"
        fileDir = os.path.dirname(__file__)
        filename = os.path.join(fileDir, 'bigthai.txt')
        with open(filename, 'r', encoding='utf-8-sig') as dict_file:
            word_list = list(set([w.rstrip() for w in dict_file.readlines()]))
            word_list.sort()
            return cls(word_list)

    def tokenize(self, s):
        """Tokenize splits a string to a list of tokens."""
        return tokenize(self.dix, s)
