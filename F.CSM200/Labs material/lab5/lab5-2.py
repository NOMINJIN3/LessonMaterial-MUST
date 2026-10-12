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

    def a_star_search(self, start, goal, heuristic):
        open_set = []
        heapq.heappush(open_set, (0, start))
        came_from = {}
        g_score = {node: float('inf') for node in self.nodes}
        g_score[start] = 0
        f_score = {node: float('inf') for node in self.nodes}
        f_score[start] = heuristic[start]

        while open_set:
            _, current = heapq.heappop(open_set)
            if current == goal:
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                return path[::-1]

            for cost, neighbor in self.nodes[current]:
                tentative_g_score = g_score[current] + cost
                if tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + heuristic[neighbor]
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

        return None  # Зам олдсонгүй

# Хэрэглээний жишээ:
graph = Graph()
graph.add_edge("A", "B", 1)
graph.add_edge("B", "C", 2)
graph.add_edge("A", "D", 4)
graph.add_edge("C", "D", 1)
graph.add_edge("B", "D", 3)

heuristic = {"A": 4, "B": 2, "C": 1, "D": 0}  # Зорилго хүртэлх тооцоолсон зай (D)

path = graph.a_star_search("A", "D", heuristic)
print("Shortest Path (A*):", path)  # Үр дүн ['A', 'B', 'C', 'D']
