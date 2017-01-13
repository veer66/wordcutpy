class PrefixTree(object):
    def __init__(self, members_with_payload):
        self.tab = {}
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
