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

class CachedSum:
    def __init__(self, total_size, sizes):
        self.total_size = total_size
        self.sizes = sizes


def partial_infection(sizes, target, epsilon):
    target = target * (1 + epsilon)
    results = [CachedSum(0, [0])]
    count = len(sizes)
    sizes.sort()
    sorted_sums = [CachedSum(s, [s]) for s in sizes]

    for key, element in enumerate(sorted_sums, start=1):
        augmented_list = [CachedSum(a.total_size + element.total_size, a.sizes + [element.total_size])
                          for a in results]
        results = merge(results, augmented_list)
        results = trim(results, delta=float(2 * epsilon) / (2 * count))
        results = [val for val in results if val.total_size <= target]
        print(results)
    return results[-1]

def merge(left, right):
    result = []
    left_idx, right_idx = 0, 0
    while left_idx < len(left) and right_idx < len(right):
        # change the direction of this comparison to change the direction of the sort
        if left[left_idx].total_size <= right[right_idx].total_size:
            result.append(left[left_idx])
            left_idx += 1
        else:
            result.append(right[right_idx])
            right_idx += 1

    if left:
        result.extend(left[left_idx:])
    if right:
        result.extend(right[right_idx:])
    return result


def trim(sizes, delta):
    last = 0
    trimmed_sizes = []
    for s in sizes:
        if s.total_size > last * (1 + delta):
            trimmed_sizes.append(s)
            last = s.total_size
    return trimmed_sizes
