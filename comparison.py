from lstar import lstar, dfa_membership
from rpni import rpni
import re
from re_generator import generate
from exrex import getone
from PySimpleAutomata import automata_IO as IO
from automata_toolkit import visual_utils
from automata_toolkit import dfa_to_regex

def rpni_dfa_reformat(dfa):
    dfa["final_states"] = dfa["accepting_states"]
    del dfa["accepting_states"]
    dfa["reachable_states"] = dfa["states"]
    dfa["final_reachable_states"] = dfa["final_states"]
    dfa["alphabets"] = dfa["alphabet"]
    del dfa["alphabet"]

    dfa["transition_function"] = {}
    for key, final_state in dfa["transitions"].items():
        initial_state, symbol = key
        if initial_state not in dfa["transition_function"]:
            dfa["transition_function"][initial_state] = { symbol : final_state }
        else:
            dfa["transition_function"][initial_state][symbol] = final_state

    dfa["states"].add("~")
    for state in dfa["states"]:
        if state not in dfa["transition_function"]:
            dfa["transition_function"][state] = {}
        for symbol in dfa["alphabets"]:
            if symbol not in dfa["transition_function"][state]:
                dfa["transition_function"][state][symbol] = "~"
    del dfa["transitions"]

    return dfa
        
def compare(dfa, true_regex):
    """Gets the F-score"""
    hypothesis_regex = dfa_to_regex.dfa_to_regex(dfa).replace("+", "|")
    print(hypothesis_regex)

    true_pos = 0
    false_pos = 0
    false_neg = 0
    for _ in range(100):
        string = getone(true_regex)
        match = re.fullmatch(hypothesis_regex, string) is not None
        if match:
            true_pos += 1
        else:
            false_neg += 1

    for _ in range(100):
        string = getone(hypothesis_regex)
        match = re.fullmatch(true_regex, string) is not None
        if match:
            true_pos += 1
        else:
            false_pos += 1
    try:
        return 2/(1/(true_pos/(true_pos + false_pos)) + 1/(true_pos/(true_pos + false_neg)))
    except:
        return 0

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
            string = getone(regex)
            res = dfa_membership(dfa, string)
            if not res:
                return False, string
            
        return True, None
    
    lstar_dfa = lstar(alphabet, string_oracle, dfa_oracle)
    rpni_dfa, _ = rpni(alphabet, s_plus, s_minus)
        
    visual_utils.draw_dfa(lstar_dfa)
    IO.dfa_to_dot(rpni_dfa, "dfa")

    rpni_dfa = rpni_dfa_reformat(rpni_dfa)
    print("L Star Regex: ")
    print("L Star FScore:", compare(lstar_dfa, regex))
    print("RPNI Regex: ")
    print("RPNI Score:", compare(rpni_dfa, regex))

if __name__ == "__main__":
    assessment("aa*", set("ab"))