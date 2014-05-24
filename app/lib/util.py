def cap(s, l):
    return s if len(s)<=l else s[0:l-3]+'...'