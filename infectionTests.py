from infection import *
import unittest

def file_to_adjacency_list(file_name):
    with open(file_name) as f:
        edges = [tuple([int(x) for x in line.split(' ')]) for line in f]
        num_vertices = edges.pop(0)[0]
        adjacency_list = [[]] * num_vertices
        for edge in edges:
            adjacency_list[edge[0]] = adjacency_list[edge[0]] + [edge[1]]
            adjacency_list[edge[1]] = adjacency_list[edge[1]] + [edge[0]]
        return adjacency_list


class TestInfection(unittest.TestCase):
    def test_components_by_size(self):
        adjacency_list = file_to_adjacency_list("tinyG.txt")
        cbs = components_by_size(adjacency_list)
        self.assertTrue(cbs[2])
        self.assertTrue(cbs[4])
        self.assertTrue(cbs[7])


    def test_total_infection(self):
        adjacency_list = file_to_adjacency_list("tinyG.txt")
        users = total_infection(adjacency_list, 8, 2.0)
        for u in users:
            if u.id == 8 or u.id == 7:
                self.assertEqual(u.version, 2.0)
            else:
                self.assertEqual(u.version, 1.0)


    def test_limited_infection(self):
        adjacency_list = file_to_adjacency_list("tinyG.txt")
        users = limited_infection(adjacency_list, 5, 2.0, .2)
        for u in users:
            if u.id in [9, 10, 11, 12]:
                self.assertEqual(u.version, 2.0)
            else:
                self.assertEqual(u.version, 1.0)


    def test_exact_limited_infection(self):
        adjacency_list = file_to_adjacency_list("tinyG.txt")

        # Passing infection
        users = exact_limited_infection(adjacency_list, 7, 2.0)
        infected_users_idx = list(range(7))
        for u in users:
            if u.id in infected_users_idx:
                self.assertEqual(u.version, 2.0)
            else:
                self.assertEqual(u.version, 1.0)

        # Failing infection
        users = exact_limited_infection(adjacency_list, 5, 2.0)
        for u in users:
            self.assertEqual(u.version, 1.0)


if __name__ == "__main__":
    unittest.main()
