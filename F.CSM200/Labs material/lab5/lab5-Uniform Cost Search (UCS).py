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

    def uniform_cost_search(self, start, goal):
        open_set = []
        heapq.heappush(open_set, (0, start))
        came_from = {}
        cost_so_far = {start: 0}

        while open_set:
            current_cost, current = heapq.heappop(open_set)

            if current == goal:
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                return path[::-1]

            for cost, neighbor in self.nodes[current]:
                new_cost = current_cost + cost
                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    came_from[neighbor] = current
                    heapq.heappush(open_set, (new_cost, neighbor))

        return None  # Зам олдсонгүй
    
#Хэрэглээний жишээ:
graph = Graph()
graph.add_edge("A", "B", 1)
graph.add_edge("B", "C", 2)
graph.add_edge("A", "D", 4)
graph.add_edge("C", "D", 1)
graph.add_edge("B", "D", 3)

path = graph.uniform_cost_search("A", "D")
print("Shortest Path (UCS):", path)  # Үр дүн: ['A', 'B', 'C', 'D']
