"""
File made for testing functions
"""

from unionfind import UnionFind
from automata_toolkit import dfa_to_regex
from automata_toolkit import visual_utils
import re

def dfa_membership(dfa, string):
    curr_state = dfa["initial_state"]
    for c in string:
        curr_state = dfa["transition_function"][curr_state][c]

    return curr_state in dfa["final_states"]

dfa = {'states': 
["[('', False), ('b', False)]", "[('', False), ('b', True)]", "[('', True), ('b', False)]"], 
'final_states': 
["[('', True), ('b', False)]"], 
'initial_state': 
"[('', False), ('b', False)]", 
'transition_function': 
{"[('', False), ('b', False)]": {'a': "[('', False), ('b', True)]", 'b': "[('', False), ('b', False)]", 'c': "[('', False), ('b', False)]"}, 
"[('', False), ('b', True)]": {'a': "[('', False), ('b', False)]", 'b': "[('', True), ('b', False)]", 'c': "[('', False), ('b', False)]"}, 
"[('', True), ('b', False)]": {'a': "[('', True), ('b', False)]", 'b': "[('', False), ('b', False)]", 'c': "[('', False), ('b', False)]"}}, 
'reachable_states': 
["[('', False), ('b', False)]", "[('', False), ('b', True)]", "[('', True), ('b', False)]"], 
'final_reachable_states': 
["[('', True), ('b', False)]"], 
'alphabets': 
['a', 'b', 'c']
}
visual_utils.draw_dfa(dfa)
regex_ = dfa_to_regex.dfa_to_regex(dfa)
res = re.fullmatch(regex_, "aba")
print(regex_, res)
print(dfa_membership(dfa, "aba"))