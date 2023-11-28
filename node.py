class Node:
    def __init__(self, parent, name, value):
        self.parent = parent
        self.name = name
        self.value = value
        self.children = []
        self.content = []

    def add(self, node):
        children.append(node)

    def rec_depth(self):
        maxdepth = 0
        for child in self.children:
            maxdepth = max(maxdepth, child.rec_depth())

        return maxdepth + 1

    def nodes_at_depth(self, k):
        stack = [(self, 0)]
        counter = 0
        while(len(stack) > 0):
            current = stack.pop()
            for child in current[0].children:
                stack.append((child, current[1] + 1))
            if(current[1] == k):
                counter += 1

        return counter

    def node_subtree_value(self, node_name):
        node = self.search_node(node_name)
        if(node is None):
            return 0

        stack = [node]
        total = 0
        while(len(stack) > 0):
            current = stack.pop()
            for child in current.children:
                stack.append(child)
            if(len(current.children) == 0):
                total += current.value

        return total

    def search_node(self, node_name):
        queue = [self]

        while(len(queue) > 0):
            current = queue.pop(0)
            if(current.name == node_name):
                return current

            for child in current.children:
                queue.append(child)

        return None

    def search_node_depth(self, node_name):
        stack = [(self, 0)]

        while(len(stack) > 0):
            current = stack.pop()
            for child in current[0].children:
                stack.append((child, current[1] + 1))
            if(current[0].name == node_name):
                return current[1]

        return -1