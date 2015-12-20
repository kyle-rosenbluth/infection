class User:
    user_index = 0
    def __init__(self, id=0, version=1.0):
        self.version = version
        self.id = id

def sampleData():
    u = []
    for i in range(0, 8):
        u.append(User(id=i, version=1.0))
    return u
users = sampleData()


adjacency_list = [
    [1, 2],
    [0],
    [0, 3],
    [2],
    [5],
    [4],
    [7],
    [6]
]

def walk(adj_list, start, process):
    """
    Performs a walk in a given adj_list starting at the start index,
    calls process(node) on each visited node.
    """
    visit_queue = {start}
    visited = set()
    while visit_queue:
        node = visit_queue.pop()
        process(node)
        visited.add(node)
        visit_queue.update(set(adj_list[node]).difference(visited))


def connected_component(node):
    """
    Takes a node id and returns the connected component that that node belongs to.
    The return value is represented as a list of node indeces.
    """
    nodes = []
    def add_node(n):
        nodes.append(n)
    walk(adjacency_list, node, add_node)
    return nodes


def components_by_size():
    """
    Returns a dictionary that maps from the size of a connected component to
    a list of elements belonging to all connected components of that size from the original graph.
    """
    indeces = list(range(len(users)))
    components = {}
    while indeces:
        component = connected_component(indeces[0])
        size = len(component)
        if size in components:
            comps_of_size = components[size]
            comps_of_size.append(indeces[0])
            components[size] = comps_of_size
        else:
            components[size] = [indeces[0]]
        indeces = [i for i in indeces if i not in component]
    return components


def total_infection(user_idx, version):
    def changeVersion(idx):
        users[idx].version = version
    walk(adjacency_list, user_idx, changeVersion)
total_infection(5, 2.5)

def trim(sizes, delta):
    last = sizes[0]
    trimmed_sizes = [last]
    for s in sizes[1:]:
        if s > last * (1 + delta):
            trimmed_sizes.append(s)
            last = s
    return trimmed_sizes


# Assumption for partial_infection. For real world use, the size of the largest connected component will be smaller than the population that we wish to infect.

print(components_by_size())
