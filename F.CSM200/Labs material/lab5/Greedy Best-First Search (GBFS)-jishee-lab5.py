import heapq

class Graph:
    def __init__(self):
        self.nodes = {}

    def add_edge(self, node1, node2, cost):
        if node1 not in self.nodes:
            self.nodes[node1] = []
        if node2 not in self.nodes:
            self.nodes[node2] = []
        self.nodes[node1].append((cost, node2))
        self.nodes[node2].append((cost, node1))  # Чиглэлгүй граф

    def greedy_best_first_search(self, start, goal, heuristic):
        open_set = []
        heapq.heappush(open_set, (heuristic[start], start))
        came_from = {}

        while open_set:
            _, current = heapq.heappop(open_set)

            if current == goal:
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                return path[::-1]

            for cost, neighbor in self.nodes[current]:
                if neighbor not in came_from:
                    came_from[neighbor] = current
                    heapq.heappush(open_set, (heuristic[neighbor], neighbor))

        return None  # Зам олдсонгүй

# Хэрэглээний жишээ:
graph = Graph()
graph.add_edge("A", "B", 1)
graph.add_edge("B", "C", 2)
graph.add_edge("A", "D", 4)
graph.add_edge("C", "D", 1)
graph.add_edge("B", "D", 3)

heuristic = {"A": 4, "B": 2, "C": 1, "D": 0}  # Зорилго хүртэлх тооцоолсон зай (D)

path = graph.greedy_best_first_search("A", "D", heuristic)
print("Path (Greedy BFS):", path)  # Үр дүн оновчтой биш байж магадгүй
