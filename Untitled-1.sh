               ||               ||b              |
               ||0              ||0              | X
a              ||0              ||1              | X
b              ||0              ||0              |
c              ||0              ||0              |
aa             ||0              ||0              |
ab             ||1              ||0              | X
ac             ||0              ||0              |
aba            ||1              ||0              | X
abb            ||0              ||0              |
abc            ||0              ||0              |
abaa           ||1              ||0              | X
abab           ||0              ||0              |
abac           ||0              ||0              |
abaaa          ||1              ||0              | X
abaab          ||0              ||0              |
abaac          ||0              ||0              |
abaaaa         ||1              ||0              |
abaaab         ||0              ||0              |
abaaac         ||0              ||0              |
{'', 'a', 'abaa', 'aba', 'ab', 'abaaa'}
{'', 'b'}

aba
{'states': s
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
