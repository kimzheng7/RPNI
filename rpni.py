"""https://faculty.ist.psu.edu/vhonavar/Papers/parekh-dfa.pdf"""

from PySimpleAutomata import automata_IO as IO
from PySimpleAutomata import DFA as DFA
import copy
from unionfind import UnionFind

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
        # Setting alphabet
        for char in word:
            dfa["alphabet"].add(char)

    return dfa    

def quotient_automaton(dfa, new_partition, non_det):
    """
    Each block = a new state, and the behaviour of each block is inherited from
    the states within the block
    """
    new_dfa = {
        "alphabet" : dfa["alphabet"],
        "states" : set(),
        "initial_state" : None,
        "accepting_states" : set(),
        "transitions" : {}
    }

    # Set representative from each partition block as the states
    for block in new_partition.components():
        new_dfa["states"].add(sorted(list(block))[0])

    # Set the initial state to be the block containing the original initial state
    # and the final states to be the blocks containing the original final states
    new_dfa["initial_state"] = sorted(list(new_partition.component(dfa["initial_state"])))[0]
    for state in dfa["accepting_states"]:
        new_dfa["accepting_states"].add(sorted(list(new_partition.component(state)))[0])

    # Inherit transitions
    non_determinism = False
    for key, new_state in dfa["transitions"].items():
        old_state, char = key

        # Find the blocks which contain old_state and new_state
        old_block = sorted(list(new_partition.component(old_state)))[0]
        new_block = sorted(list(new_partition.component(new_state)))[0]

        if non_det:
            if (old_block, char) not in new_dfa["transitions"]:
                new_dfa["transitions"][(old_block, char)] = set()
            elif new_block not in new_dfa["transitions"][(old_block, char)]:
                non_determinism = True
            new_dfa["transitions"][(old_block, char)].add(new_block)
        else:
            if (old_block, char) in new_dfa["transitions"] and (new_block != new_dfa["transitions"][(old_block, char)]):
                non_determinism = True
                raise ValueError()
            new_dfa["transitions"][(old_block, char)] = new_block

    return new_dfa, non_determinism
        
def rpni(s_plus, s_minus):
    # Step 1: Construct the Prefix Tree Acceptor
    dfa = pta(s_plus)
    states = list(dfa["states"])
    states.sort()
    states.sort(key = len)

    # Step 2: Iteratively merge partition
    # Step 2a: Every state is in it's own block first
    current_partition = UnionFind(states)

    # Step 2b: Merge the partition blocks that different states belong to
    for i in range(1, len(states)):
        for j in range(i):            
            # Merge the two blocks
            new_partition = copy.deepcopy(current_partition)
            new_partition.union(states[i], states[j])

            # Step 2c: Get the quotient automaton for this partition
            new_dfa, non_det = quotient_automaton(dfa, new_partition, True)

            # Step 2d: Merge the non-deterministic blocks
            while non_det:
                for val in new_dfa["transitions"].values():
                    val = list(val)

                    if len(val) == 1:
                        continue
                    for k in range(len(val) - 1):
                        new_partition.union(val[k], val[k + 1])

                new_dfa, non_det = quotient_automaton(dfa, new_partition, True)

            # Step 3: Verify that resultant quotient automata is consistent with negative examples
            new_dfa, _ = quotient_automaton(dfa, new_partition, False)
            valid = True
            for neg in s_minus:
                if DFA.dfa_word_acceptance(new_dfa, neg):
                    valid = False

            if valid:
                current_partition = new_partition
                break

    return quotient_automaton(dfa, current_partition, False)


if __name__ == "__main__":
    s_plus = ["b", "aa", "aaaa"]
    s_minus = ["", "a", "aaa", "baa"]
    dfa, _ = rpni(s_plus, s_minus)
    IO.dfa_to_dot(dfa, "dfa")
