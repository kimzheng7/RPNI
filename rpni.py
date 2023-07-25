"""https://faculty.ist.psu.edu/vhonavar/Papers/parekh-dfa.pdf"""

from automata.fa.dfa import DFA
from automata.fa.nfa import NFA
import copy
from unionfind import UnionFind

def pta(alphabet, s_plus):
    states = set()
    states.add("")
    input_symbols = alphabet
    transitions = {}
    initial_state = ""
    final_states = set()

    # States are prefixes of words in s_plus
    for word in s_plus:
        for i in range(len(word) + 1):
            if i == len(word):
                transitions[word] = {}
            prefix = word[0 : i + 1]
            states.add(prefix)
            transitions[prefix[:-1]] = { prefix[-1]: prefix }

    # Accepting states are words in s_plus
    for word in s_plus:
        final_states.add(word)

    return DFA(
        states = states,
        input_symbols = input_symbols,
        transitions = transitions,
        initial_state = initial_state,
        final_states = final_states,
        allow_partial = True
    )    

def quotient_automaton(dfa, new_partition, non_det):
    """
    Each block = a new state, and the behaviour of each block is inherited from
    the states within the block
    """
    states = set()
    input_symbols = dfa.input_symbols
    transitions = {}
    initial_state = None
    final_states = set()

    # Set representative from each partition block as the states
    for block in new_partition.components():
        states.add(sorted(list(block))[0])
        transitions[sorted(list(block))[0]] = {}

    # Set the initial state to be the block containing the original initial state
    # and the final states to be the blocks containing the original final states
    initial_state = sorted(list(new_partition.component(dfa.initial_state)))[0]
    for state in dfa.final_states:
        final_states.add(sorted(list(new_partition.component(state)))[0])

    # Inherit transitions
    non_determinism = False
    for old_state, output in dfa.transitions.items():
        for char, new_state in output.items():
            # Find the blocks which contain old_state and new_state
            old_block = sorted(list(new_partition.component(old_state)))[0]
            new_block = sorted(list(new_partition.component(new_state)))[0]

            if non_det:
                if old_block not in transitions:
                    transitions[old_block] = {}
                if char not in transitions[old_block]:
                    transitions[old_block][char] = set()
                elif new_block not in transitions[old_block][char]:
                    non_determinism = True
                transitions[old_block][char].add(new_block)
            else:
                if old_block not in transitions:
                    transitions[old_block] = {}
                if char in transitions[old_block] and new_block != transitions[old_block][char]:
                    raise ValueError("Shouldn't be any non determinism")
                transitions[old_block][char] = new_block

    if non_det:
        return NFA(
            states = states,
            input_symbols = input_symbols,
            transitions = transitions,
            initial_state = initial_state,
            final_states = final_states
        ), non_determinism
    else:
        return DFA(
            states = states,
            input_symbols = input_symbols,
            transitions = transitions,
            initial_state = initial_state,
            final_states = final_states,
            allow_partial = True            
        ), non_determinism
        
def rpni(alphabet, s_plus, s_minus):
    # Step 1: Construct the Prefix Tree Acceptor
    dfa = pta(alphabet, s_plus)
    states = list(dfa.states)
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
            new_nfa, non_det = quotient_automaton(dfa, new_partition, True)

            # Step 2d: Merge the non-deterministic blocks
            while non_det:
                for output in new_nfa.transitions.values():
                    for val in output.values():
                        val = list(val)

                        if len(val) == 1:
                            continue
                        for k in range(len(val) - 1):
                            new_partition.union(val[k], val[k + 1])

                new_nfa, non_det = quotient_automaton(dfa, new_partition, True)

            # Step 3: Verify that resultant quotient automata is consistent with negative examples
            new_dfa, _ = quotient_automaton(dfa, new_partition, False)
            valid = True
            for neg in s_minus:
                if new_dfa.accepts_input(neg):
                    valid = False

            if valid:
                current_partition = new_partition
                break

    return quotient_automaton(dfa, current_partition, False)

if __name__ == "__main__":
    from re_generator import generate
    import random
    import re
    pos_samples = ["b", "aa", "aaaa"]
    neg_samples = ["", "a", "aaa", "baa"]
    alphabet = set("ab")

    # any = "(a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z|?|!| )"
    # regex = "hello!* are you okay?+ ye(p|a)+"
    # alphabet = set("heloaryukp !?")

    # pos_samples = []
    # neg_samples = []
    # for i in range(200):
    #     if random.choice([True, False]):
    #         # Generate random string
    #         string = generate(any)
    #         match = re.fullmatch(regex, string) is not None
    #         if match:
    #             pos_samples.append(string)
    #         else:
    #             neg_samples.append(string)
    #     else:
    #         pos_samples.append(generate(regex))

    dfa, _ = rpni(alphabet, pos_samples, neg_samples)
    dfa.show_diagram()
