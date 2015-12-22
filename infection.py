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


sample_adjacency_list = [
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


def connected_component(adj_list, node):
    """
    Takes a node id and returns the connected component that that node belongs to.
    The return value is represented as a list of node indices.
    """
    nodes = []
    def add_node(n):
        nodes.append(n)
    walk(adj_list, node, add_node)
    return nodes


def components_by_size(adj_list):
    """
    Returns a dictionary that maps from the size of a connected component to
    a list of elements belonging to all connected components of that size from the original graph.
    """
    indices = list(range(len(adj_list)))
    components = {}
    while indices:
        component = connected_component(adj_list, indices[0])
        size = len(component)
        if size in components:
            comps_of_size = components[size]
            comps_of_size.append(indices[0])
            components[size] = comps_of_size
        else:
            components[size] = [indices[0]]
        indices = [i for i in indices if i not in component]
    return components


def total_infection(adj_list, user_idx, version):
    def changeVersion(idx):
        users[idx].version = version
    walk(adj_list, user_idx, changeVersion)


class CachedSum:
    def __init__(self, total_size, sizes):
        self.total_size = total_size
        self.sizes = sizes

def limited_infection(adj_list, target, version, epsilon):
    comps = components_by_size(adj_list)
    sizes = []
    for k in comps.keys():
        sizes.extend([k for z in comps[k]])
    cachedSum = partial_infection(sizes, target, epsilon)
    if cachedSum is not None:
        for partial in cachedSum.sizes:
            node = comps[partial].pop()
            total_infection(adj_list, node, version)
    else:
        print("FAILED")



def partial_infection(sizes, target, epsilon):
    results = [CachedSum(0, [])]
    count = len(sizes)
    sizes.sort()
    sorted_sums = [CachedSum(s, [s]) for s in sizes]
    for key, element in enumerate(sorted_sums, start=1):
        augmented_list = [CachedSum(a.total_size + element.total_size, a.sizes + [element.total_size])
                          for a in results]
        results = merge(results, augmented_list)
        results = [val for val in results if val.total_size <= target * (1 + epsilon)]

    closest = min(results, key=lambda x: abs(x.total_size - target))
    if abs(closest.total_size - target) <= target * epsilon:
        return closest
    return None

def merge(left, right):
    result = []
    left_idx, right_idx = 0, 0
    while left_idx < len(left) and right_idx < len(right):
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

if __name__ == "__main__":
    limited_infection(sample_adjacency_list, target=5, version=2.0, epsilon=0.3)
    for u in users:
        print(u.version)
