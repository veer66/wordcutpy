# Copyright (c) 2015, Vee Satayamas
# All rights reserved.

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:

# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.

# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import re

LEFT = 1
RIGHT = 2

UNK   = 1
DICT  = 2
INIT  = 3
LATIN = 4
PUNC  = 5

class Wordcut(object):
    def __init__(self, wordlist):
        self.wordlist = wordlist

    def seek(self, l, r, ch, str_offset, pos):
        ans = None
        while l <= r:
            m = (l + r) / 2
            dict_item = self.wordlist[m]
            word_len = len(dict_item)
            if word_len <= str_offset:
                l = m + 1;
            else:
                ch_ = dict_item[str_offset]
                if ch_ < ch:
                    l = m + 1
                elif ch_ > ch:
                    r = m - 1
                else:
                    ans = m
                    if pos == LEFT:
                        r = m - 1
                    else:
                        l = m + 1
        return ans

    def is_better(self, link0, link1):
        if link0 is None:
            return True

        if link1["unk"] < link0["unk"]:
            return True
        
        if link1["w"] < link0["w"]:
            return True
        
        return False

    def build_path(self, s):
        left_boundary = 0
        dict_acc_list = []
        
        path = [{"p":None, "w": 0, "unk": 0, "type": INIT}]
        
        latin_s = None
        latin_e = None
        
        punc_s = None
        punc_e = None
        
        for i in range(len(s)):
            dict_acc_list.append({"s":i, "l": 0, "r": len(self.wordlist)-1})
            ch = s[i]
            
            # Update dict acceptors
            _dict_acc_list = dict_acc_list
            dict_acc_list = []                        
            for acc in _dict_acc_list:
                l = self.seek(acc["l"], acc["r"], ch, i-acc["s"], LEFT)
                if l is not None:
                    is_final = len(self.wordlist[l]) == i - acc["s"] + 1
                    r = self.seek(l, acc["r"], ch, i-acc["s"], RIGHT)
                    dict_acc_list.append({"s":acc["s"], "l": l, "r": r, "final":is_final})
            
            
            # latin words
            if latin_s is None:
                if re.match(u"[A-Za-z]", ch):
                    latin_s = i
                    
            if latin_s is not None:            
                if re.match(u"[A-Za-z]", ch):
                    if i + 1 == len(s) or re.match(u"[A-Za-z]", s[i + 1]):
                        latin_e = i
                else:
                    latin_s = None
                    latin_e = None
            
            # puncuation
            if punc_s is None:
                if ch == " ":
                    punc_s = i
 
            if punc_s is not None:
                if ch == " ":
                    if len(s) == i + 1 or s[i + 1] != " ":
                        punc_e = i
                else:
                    punc_s = None
                    punc_e = None
            
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
                    if self.is_better(link, _link):
                        link = _link
                        
            # link from latin word
            if latin_s is not None and latin_e is not None:
                p_link = path[latin_s]
                _link = {"p": latin_s, 
                         "w": p_link["w"] + 1, 
                         "unk": p_link["unk"],
                         "type": LATIN}
                if self.is_better(link, _link):
                    link = _link
                                
            # link from puncuation
            if punc_s is not None and punc_e is not None:                
                p_link = path[punc_s]
                _link = {"p": punc_s, 
                         "w": p_link["w"] + 1, 
                         "unk": p_link["unk"],
                         "type": PUNC}
                if self.is_better(link, _link):
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
                left_boundary = i
        return path
    
    def path_to_tokens(self, txt, path):
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
    
    def tokenize(self, s):
        path = self.build_path(s)
        tokens = self.path_to_tokens(s, path)
        return tokens
