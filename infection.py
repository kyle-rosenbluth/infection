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
        for child in adj_list[node]:
            if child not in visited:
                visit_queue.add(child)

def total_infectioin(user_idx, version):
    walk(adj_list, user_idx, lambda u: users[u].version = version)
