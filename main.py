from ressources_mars import START_POINT, END_POINT, DISTANCES_DES_LIAISONS


class Dijkstra:
    def __init__(self, start: str, end: str):
        self.start_point = start
        self.end_point = end
        self.min_costs = {self.start_point: 0}
        self.previous_nodes = {}
        self.links = self.precompute_links()

    def __call__(self):
        nodes_to_visit = [(0, self.start_point)]
        visited = set()

        while nodes_to_visit:
            nodes_to_visit.sort()

            current_cost, current_node = nodes_to_visit.pop(0)

            if current_node in visited:
                continue

            visited.add(current_node)

            if current_node == self.end_point:
                path: list[str] = self.reconstruct_path()
                print(f"Chemin le plus court: {' → '.join(path)} avec un coût de {round(current_cost / 1000, 2)}km")

            for letter, distance in self.get_letters_around(current_node):
                new_cost: int = current_cost + distance

                if letter not in self.min_costs or new_cost < self.min_costs[letter]:
                    self.min_costs[letter] = new_cost
                    self.previous_nodes[letter] = current_node
                    nodes_to_visit.append((new_cost, letter))

    def reconstruct_path(self) -> list[str]:
        path = []
        current_node = self.end_point
        while current_node != self.start_point:
            path.append(current_node)
            current_node = self.previous_nodes[current_node]
        path.append(self.start_point)

        return path[::-1]

    def get_letters_around(self, letter: str) -> list[tuple[str, int]]:
        return self.links.get(letter, [])

    @staticmethod
    def precompute_links() -> dict[str, list[tuple[str, int]]]:
        links = {}
        for (letter1, letter2), distance in DISTANCES_DES_LIAISONS:
            if letter1 not in links:
                links[letter1] = []
            links[letter1].append((letter2, distance))

            if letter2 not in links:
                links[letter2] = []
            links[letter2].append((letter1, distance))
        return links


if __name__ == '__main__':
    for letter_start in START_POINT:
        dijkstra = Dijkstra(letter_start, END_POINT)
        dijkstra()
