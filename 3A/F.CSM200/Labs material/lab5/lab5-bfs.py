from collections import deque

class Graph:
    def __init__(self):
        self.nodes = {}

    def add_edge(self, node1, node2):
        if node1 not in self.nodes:
            self.nodes[node1] = []
        if node2 not in self.nodes:
            self.nodes[node2] = []
        self.nodes[node1].append(node2)
        self.nodes[node2].append(node1)  # Чиглэлгүй граф

    def bfs(self, start, goal):
        queue = deque([[start]])
        visited = set()

        while queue:
            path = queue.popleft()
            node = path[-1]

            if node in visited:
                continue
            visited.add(node)

            if node == goal:
                return path  # Хамгийн богино замыг оллоо

            for neighbor in self.nodes.get(node, []):
                new_path = list(path)
                new_path.append(neighbor)
                queue.append(new_path)

        return None  # Зам олдсонгүй

# Хэрэглээний жишээ:
graph = Graph()
graph.add_edge("A", "B")
graph.add_edge("A", "C")
graph.add_edge("B", "D")
graph.add_edge("C", "E")
graph.add_edge("D", "E")

path = graph.bfs("A", "E")
print("Хамгийн богино зам (BFS)аргаар:", path)  # Үр дүн: ['A', 'C', 'E']
