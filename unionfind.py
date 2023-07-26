class UnionFind:
    def __init__(self, elements):
        self.elements = elements
        self.components = {}

        for element in elements:
            self.components[element] = [element]

    def union(self, elem_one, elem_two):
        if self.components[elem_one] == self.components[elem_two]:
            return

        self.components[elem_one] += self.components[elem_two]
        for element in self.components[elem_one]:
            self.components[element] = self.components[elem_one]

    def component(self, elem):
        return self.components[elem]
    
    def components_list(self):
        return self.components.values()