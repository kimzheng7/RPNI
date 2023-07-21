def dict_to_s(dict):
    return str(sorted(dict.items()))

def format_table(T):
    print("{:<15}".format("") + "|", end = "")
    # columns
    for key in sorted(T[""].keys()):
        print("|" + "{:<15}".format(key) + "|", end = "")
    print()

    # rows
    for row in T:
        print("{:<15}".format(row) + "|", end = "")
        for key in sorted(T[row].keys()):
            print("|" + "{:<15}".format(int(T[row][key])) + "|", end = "")
        print()

def dfa_membership(dfa, string):
    curr_state = dfa["initial_state"]
    for c in string:
        curr_state = dfa["transition_function"][curr_state][c]

    return curr_state in dfa["final_states"]

def separable_check(T, S, alphabet):
    # checks that all prefix rows are different (if any 2 same, then prefix + a rows same too)
    for prefix_one in S:
        for prefix_two in S:
            if prefix_one == prefix_two:
                continue
            
            if T[prefix_one] == T[prefix_two]:
                for a in alphabet:
                    if T[prefix_one + a] != T[prefix_two + a]:
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

def table_to_DFA(alphabet, S, E, T):
    # every prefix is a state
    states = []
    for pref in S:
        if dict_to_s(T[pref]) not in states:
            states.append(dict_to_s(T[pref]))
    # prefixes which are accepted are final states
    final_states = []
    for pref in S:
        if T[pref][""] and dict_to_s(T[pref]) not in final_states:
            final_states.append(dict_to_s(T[pref]))

    initial_state = dict_to_s(T[""])
    # for each prefix, see the prefix + a which has the same row. add 'a' transition
    transition_function = {}
    for pref in S:
        for a in alphabet:
            if dict_to_s(T[pref]) not in transition_function:
                transition_function[dict_to_s(T[pref])] = {a : dict_to_s(T[pref + a])}
            else:
                transition_function[dict_to_s(T[pref])][a] = dict_to_s(T[pref + a])

    return {
        "states" : states,
        "final_states" : final_states,
        "initial_state" : initial_state,
        "transition_function" : transition_function,
        "reachable_states": states,
        "final_reachable_states": final_states,
        "alphabets": list(alphabet)
    }

def lstar(alphabet, string_oracle, dfa_oracle):
    S = set() # prefix set
    E = set() # suffix set
    S.add("")
    E.add("")
    T = {} # table storing (prefix \cup prefix + \Sigma) . (E)
    
    T[""] = {"" : string_oracle("")}
    for a in alphabet:
        T[a] = {"" : string_oracle(a)}

    while True:
        separable, nonsep_one, nonsep_two = separable_check(T, S, alphabet)
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
                                    T[pref][a + suff] = string_oracle(pref + a + suff)
                                    for b in alphabet:
                                        T[pref + b][a + suff] = string_oracle(pref + b + a + suff)
                                break

            if not closed:
                # add the nonclosed row as a new prefix
                S.add(nonclosed_prefix + nonclosed_symbol)

                # fill in table accordingly with prefix + a
                for a in alphabet:
                    cols = {}
                    for suff in E:
                        cols[suff] = string_oracle(nonclosed_prefix + nonclosed_symbol + a + suff)
                    T[nonclosed_prefix + nonclosed_symbol + a] = cols
                # fill in table with prefix
                cols = {}
                for suff in E:
                    cols[suff] = string_oracle(nonclosed_prefix + nonclosed_symbol + suff)
                T[nonclosed_prefix + nonclosed_symbol] = cols

            separable, nonsep_one, nonsep_two = separable_check(T, S, alphabet)
            closed, nonclosed_prefix, nonclosed_symbol = closed_check(T, S, alphabet)

        dfa = table_to_DFA(alphabet, S, E, T)
        equal, counterexample = dfa_oracle(dfa)
        if equal:
            break
        
        for i in range(0, len(counterexample) + 1):
            S.add(counterexample[0 : i])
            # fill table with row prefix = counterexample[0 : i]
            if counterexample[0 : i] not in T:
                T[counterexample[0 : i]] = {}
            for suff in E:
                T[counterexample[0 : i]][suff] = string_oracle(counterexample[0 : i] + suff)
            # fill with prefix + a
            for a in alphabet:
                if (counterexample[0 : i] + a) not in T:
                    T[counterexample[0 : i] + a] = {}
                for suff in E:
                    T[counterexample[0 : i] + a][suff] = string_oracle(counterexample[0 : i] + a + suff)
                
    return dfa

if __name__ == "__main__":
    import re
    from automata_toolkit import dfa_to_regex
    from automata_toolkit import visual_utils
    from re_generator import generate

    def generate_oracles(regex):
        def string_oracle(string):
            res = re.fullmatch(regex, string)
            return res is not None
        
        def dfa_oracle(dfa):
            for _ in range(100):
                string = generate(regex)
                res = dfa_membership(dfa, string)
                if not res:
                    return False, string
                
            return True, None
        
        return string_oracle, dfa_oracle
    
    alphabet = set("abc")
    regex = "aba*"

    string_oracle, dfa_oracle = generate_oracles(regex)
    dfa = lstar(alphabet, string_oracle, dfa_oracle)
    # visual_utils.draw_dfa(dfa)
    print(dfa_to_regex.dfa_to_regex(dfa)) # Function is buggy