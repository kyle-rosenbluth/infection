class User:
    user_index = 0
    def __init__(self, id, version=1.0):
        self.version = version
        self.id = id

adjacency_list = [
    [1, 2, 3],
    [0, 3],
    [0],
    [0, 1]
]

def walk(adj_list, start, visit):
    visit_queue = {start}
    visited = set()
    while visit_queue:
        node = visit_queue.pop()
        visit(node)
        visited.add(node)
        visit_queue.update(set(adj_list[node]).difference(visited))

def total_infection(user_idx, version):
    walk(adjacency_list, user_idx, lambda u: None)
