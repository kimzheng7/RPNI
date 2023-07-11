from PySimpleAutomata import automata_IO as IO

def pta(s_plus):
    dfa = {
        "alphabet" : set(),
        "states" : set(),
        "initial_state" : "",
        "accepting_states" : set(),
        "transitions" : {}
    }
    dfa["states"].add("")

    # States are prefixes of words in s_plus
    for word in s_plus:
        for i in range(len(word)):
            prefix = word[0 : i + 1]
            dfa["states"].add(prefix)
            dfa["transitions"][(prefix[:-1], prefix[-1])] = prefix

    # Accepting states are words in s_plus
    for word in s_plus:
        dfa["accepting_states"].add(word)

    return dfa    


def rpni(s_plus, s_minus):
    # Step 1: Construct the Prefix Tree Acceptor
    dfa = pta(s_plus)

    return dfa


if __name__ == "__main__":
    s_plus = ["a", "abb", "bba", "bbb"]
    s_minus = ["b", "aa", "bb", "baba"]
    dfa = rpni(s_plus, s_minus)
    print(dfa)
    IO.dfa_to_dot(dfa, "dfa")
