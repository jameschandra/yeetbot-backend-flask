def kmp_border_function(pattern,j):
    k = j-1
    if k < 0:
        return -1
    elif k == 0:
        return 0
    else:

        prefix_array = []
        suffix_array = []
        prefix = ""
        suffix = ""
        to_return = 0
        for i in range(k):
            prefix += pattern[i]
            prefix_array.append(prefix)
        for j in range(k,0,-1):
            suffix = pattern[j] + suffix
            suffix_array.append(suffix)
        for l in range(len(prefix_array)):
            if prefix_array[l] == suffix_array[l]:
                to_return = len(prefix_array[l])
        return to_return

def make_kmp_table(kmp_table,pattern):
    for i in range(len(pattern)):
        kmp_table.append(kmp_border_function(pattern,i))

def kmp(text,pattern,kmp_table):
    make_kmp_table(kmp_table,pattern)
    i = 0
    j = 0
    # for i in range(len(text)):
    while j < len(pattern) and i < len(text):
        # mismatch or j = len(pattern) or i = len(text)
        if text[i] == pattern[j]:
            i += 1
            j += 1
        elif text[i] != pattern[j]:
            if j == 0:
                i += 1
            else:
                j = kmp_table[j]
    if j == len(pattern): # matching
        return i - j
    else: # no match
        return -1