Dependencies are 
- `pysimpleautomata`
- `pyunionfind`
- `automata-toolkit`
`pip install` all of these before beginning 

To run RPNI, go to rpni.py, and change the `re` variable. The program will generate positive examples of the regular expression.
You will also have to provide your own negative examples in the `neg_samples` variable. Running
`python3 rpni.py`
will then learn the regular expression based on the examples.

To run L*, go to lstar.py, and change the `alphabet` and `regex` variables to what you need. Running
`python3 lstar.py`
will then learn the regular expression by querying the regex provided.