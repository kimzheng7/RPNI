from lstar import lstar
from rpni import rpni
import re
from automata_toolkit import dfa_to_regex
from automata_toolkit import visual_utils
from re_generator import generate

def assessment(regex, alphabet):
    s_plus = []
    s_minus = []

    # create two oracles
    def string_oracle(string):
        res = re.fullmatch(regex, string)
        match = res is not None
        if match:
            s_plus.append(string)
        else:
            s_minus.append(string)

        return match
    
    def dfa_oracle(dfa):
        for _ in range(100):
            string = generate(regex)
            res = dfa_membership(dfa, string)
            if not res:
                return False, string
            
        return True, None
    
    lstar_dfa = lstar(alphabet, string_oracle, dfa_oracle)
    rpni_dfa, _ = rpni(alphabet, s_plus, s_minus)
        
