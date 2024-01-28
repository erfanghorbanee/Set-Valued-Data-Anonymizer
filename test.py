import unittest

from models.gentree import GenTree
from partition_for_transaction import list_to_str, partition

ATT_TREE = {}


def init_tree():
    global ATT_TREE
    ATT_TREE = {}
    root = GenTree("*")
    ATT_TREE["*"] = root
    lt = root.add_node("A")
    ATT_TREE["A"] = lt
    ATT_TREE["a1"] = lt.add_node("a1", True)
    ATT_TREE["a2"] = lt.add_node("a2", True)
    rt = root.add_node("B")
    ATT_TREE["B"] = rt
    ATT_TREE["b1"] = rt.add_node("b1", True)
    ATT_TREE["b2"] = rt.add_node("b2", True)


class test_partition(unittest.TestCase):
    def test_case_from_paper(self):
        init_tree()

        # original transaction
        trans = [
            ["a1"],
            ["a1", "a2"],
            ["b1", "b2"],
            ["b1", "b2"],
            ["a1", "a2", "b2"],
            ["a1", "a2", "b2"],
            ["a1", "a2", "b1", "b2"],
        ]
        result, _ = partition(ATT_TREE, trans, 2)
        for i, t in enumerate(result[:]):
            result[i] = list_to_str(t)
        print(result)
        self.assertEqual(
            set(result),
            set(["A", "A", "a1;a2;B", "a1;a2;B", "a1;a2;B", "b1;b2", "b1;b2"]),
        )


if __name__ == "__main__":
    unittest.main()
