def separable_check(T, S):
    # checks that all prefix rows are different
    for prefix_one in S:
        for prefix_two in S:
            if prefix_one == prefix_two:
                continue
            
            if T[prefix_one] == T[prefix_two]:
                return False, prefix_one, prefix_two
            
    return True, None, None

def closed_check(T, S, alphabet):
    # checks that each prefix + alphabet rows have an identical prefix row
    for a in alphabet:
        for prefix_one in S:
            identical_exists = False
            for prefix_two in S:
                if T[prefix_one + a] == T[prefix_two]:
                    identical_exists = True

            if not identical_exists:
                return False, prefix_one, a

    return True, None, None

def lstar(alphabet, oracle):
    S = set("") # prefix set
    E = set("") # suffix set
    T = {} # table storing (prefix \cup prefix + \Sigma) . (E)
    
    T[""] = {"" : oracle("")}
    for a in alphabet:
        T[a] = {"" : oracle(a)}

    separable, nonsep_one, nonsep_two = separable_check(T, S)
    closed, nonclosed_prefix, nonclosed_symbol = closed_check(T, S, alphabet)
    while not (separable and closed):
        if not separable:
            # find a symbol which causes them to differ
            for a in alphabet:
                if T[nonsep_one + a] != T[nonsep_two + a]:
                    for suff in E:
                        # when we find symbol + suffix which causes them to differ, add this to suffix list
                        if T[nonsep_one + a][suff] != T[nonsep_two + a][suff]:
                            E.add(a + suff)
                            for pref in S:
                                T[pref][a + suff] = oracle(pref + a + suff)
                                for b in alphabet:
                                    T[pref + b][a + suff] = oracle(pref + b + a + suff)

                            break


        if not closed:
            # add the nonclosed row as a new prefix
            S.add(nonclosed_prefix + nonclosed_symbol)

            # fill in table accordingly
            cols = {}
            for suff in E:
                cols[suff] = oracle(nonclosed_prefix + nonclosed_symbol + suff)
            T[nonclosed_prefix + nonclosed_symbol] = cols

        separable, nonsep_one, nonsep_two = separable_check(T, S)
        closed, nonclosed_prefix, nonclosed_symbol = closed_check(T, S, alphabet)

    print(T)


if __name__ == "__main__":
    import re
    def oracle(string):
        res = re.fullmatch("a*", string)
        return res is not None
    
    lstar(set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"), oracle)