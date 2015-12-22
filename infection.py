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
#-------------------------------------------------------------------------------
def walk(adj_list, start, process):
    """
    Performs a breadth first walk in a given graph represented by an
    adjacency list starting at the start index and calls process(node)
    on each visited node.
    Args:
        adj_list ([[int]])
        start (int)           : the starting node for the walk
        process (int -> None) : a func that's called on all nodes in the walk
    Returns:
        None
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
    Takes a node and returns the connected component that that node belongs to.
    Args:
        adj_list ([[int]])
        node (int)
    Returns:
        [int] : a list of all nodes in the connected component
    """
    nodes = []
    def add_node(n):
        nodes.append(n)
    walk(adj_list, node, add_node)
    return nodes

#-------------------------------------------------------------------------------

def components_by_size(adj_list):
    """
    Args:
        adj_list ([[int]])
    Returns:
        {int: [int]}: a dictionary whose keys are the size of the connected
                      components and values are a list of nodes, each one
                      belonging to a different connected component of that size.
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


def total_infection(adj_list, start, version):
    """
    Performs a total infection, starting from a single user,
    and changing the version of all users that are connected to
    the given user.
    Args:
        adj_list ([[int]])
        start (int)       : the starting index of the infection
        version (float)   : the version to change all infected users to
    Returns:
        None
    """
    def changeVersion(idx):
        users[idx].version = version
    walk(adj_list, start, changeVersion)


class CachedSum:
    def __init__(self, total_size, sizes):
        self.total_size = total_size
        self.sizes = sizes

def exact_limited_infection(adj_list, target, version):
    limited_infection(adj_list, target, version, epsilon=0.0)

def limited_infection(adj_list, target, version, epsilon):
    """
    Performs an infection that aims to infect a target # of users.
    Args:
        adj_list ([[int]])
        target (int)      : the goal number of users to infect
        version (float)   : the version to change all infected users to
        epsilon (float)   : the acceptable percent error (+/- epsilon percent)
    Returns:
        None
    """
    comps = components_by_size(adj_list)
    sizes = []
    for k in comps.keys():
        sizes.extend([k for z in comps[k]])

    cachedSum = None
    if epsilon == 0:
        cachedSum = exact_sum(sizes, target)
    else:
        cachedSum = subset_sum(sizes, target, epsilon)
    if cachedSum:
        for partial in cachedSum.sizes:
            node = comps[partial].pop()
            total_infection(adj_list, node, version)
    else:
        print("FAILED")


def subset_sum(sizes, target, epsilon):
    """
    Given a list of sizes, tries to find sizes that sum to a target.
    Args:
        sizes ([int])
        target (int)
        epsilon (float) : the acceptable percent error (+/- epsilon percent)
    Returns:
        CachedSum unless it couldn't find sizes within epsilon,
        in which case it returns None
    """
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
    """
    Merges and sorts two sorted lists.
    Args:
        left ([CachedSum])
        right ([CachedSum])
    Returns:
        [CachedSum]
    """
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
    """
    Takes a list of CachedSum's and a delta and removes CachedSum's whose values
    are closer together than delta percent.
    Args:
        sizes ([CachedSum])
        delta (float)      : Acceptable percent difference for two elements to be considered separate
    Returns:
        [CachedSum]
    """
    last = 0
    trimmed_sizes = []
    for s in sizes:
        if s.total_size > last * (1 + delta):
            trimmed_sizes.append(s)
            last = s.total_size
    return trimmed_sizes


def exact_sum(sizes, target):
    # Q(i, t) := q(i - 1, t) or (s_i == t) or Q(i - 1, t - s_i)

    # Initialize the table of len(sizes) by target + 1
    table = [x[:] for x in [[[]]*(target + 1)]*len(sizes)]
    for i, s in enumerate(sizes):
        for t in range(target + 1):
            if s == t:
                table[i][t] = [s]
            elif i > 0 and t >= s and table[i - 1][t - s]:
                table[i][t] = table[i - 1][t - s] + [s]
            elif i > 0 and table[i - 1][t]:
                table[i][t] = table[i - 1][t]
            else:
                table[i][t] = []
    return CachedSum(target, table[-1][-1])

if __name__ == "__main__":
    limited_infection(sample_adjacency_list, target=5, version=2.0, epsilon=0.3)
    for u in users:
        print(u.version)
    sizes = [10, 11, 12, 15, 20, 21, 22, 23, 24, 29]
    print(exact_sum(sizes, 17))
