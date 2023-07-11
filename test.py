from unionfind import UnionFind

states = [1, 2, 3, 4, 5, 6]

for i in range(1, len(states)):
    for j in range(i):
        print(i, j)