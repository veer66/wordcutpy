import re

class PrefixTree(object):
    def __init__(self, members_with_payload):
        self.tab = {}
        if members_with_payload is None:
            return 
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
        key = (i, offset, member)
        if key not in self.tab:
            return None
        return self.tab[key]

UNK   = 1
DICT  = 2
INIT  = 3
LATIN = 4
PUNC  = 5

def is_better(link0, link1):
    if link0 is None:
        return True

    if link1["unk"] < link0["unk"]:
        return True

    if link1["w"] < link0["w"]:
        return True

    return False


class LatinTransducer:
    def __init__(self):
        self.latin_s = None
        self.latin_e = None

    def update(self, ch, i, s):
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
        if self.latin_s is not None and self.latin_e is not None:
            p_link = path[self.latin_s]
            _link = {"p": self.latin_s, 
                     "w": p_link["w"] + 1, 
                     "unk": p_link["unk"],
                     "type": LATIN}
            return _link
        return None

class PuncTransducer:
    def __init__(self):
        self.punc_s = None
        self.punc_e = None

    def update(self, ch, i, s):
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
        if self.punc_s is not None and self.punc_e is not None:                
            p_link = path[self.punc_s]
            _link = {"p": self.punc_s, 
                     "w": p_link["w"] + 1, 
                     "unk": p_link["unk"],
                     "type": PUNC}
            return _link
        return None

def build_path(dix, s):
    left_boundary = 0
    dict_acc_list = []

    path = [{"p":None, "w": 0, "unk": 0, "type": INIT}]

    punc_transducer = PuncTransducer()
    latin_transducer = LatinTransducer()
    
    for i, ch in enumerate(s):
        dict_acc_list.append({"s":i, "p":0, "final":False})

        # Update dict acceptors
        _dict_acc_list = dict_acc_list
        dict_acc_list = []                        
        for acc in _dict_acc_list:
            offset = i - acc["s"]
            child = dix.lookup(acc["p"], offset, ch)
            if child is not None:
                child_p, is_final, payload = child
                dict_acc_list.append({"s":acc["s"], "p": child_p,
                                      "final":is_final})
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
    if txt is None or txt == "":
        return []
    path = build_path(dix, txt)
    return path_to_tokens(txt, path)

class Wordcut(object):
    def __init__(self, wordlist):
        self.dix = PrefixTree([(word, None) for word in wordlist])


    @classmethod
    def bigthai(cls):
        import os
        "Initialize from bigthai"
        fileDir =  os.path.dirname(__file__)
        filename = os.path.join(fileDir, 'bigthai.txt')
        with open(filename) as dict_file:

            word_list = list(set([w.rstrip() for w in dict_file.readlines()]))
            word_list.sort()
            return cls(word_list)

    def tokenize(self, s):
        return tokenize(self.dix, s)
