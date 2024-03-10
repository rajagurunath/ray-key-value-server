import ray


@ray.remote
class BTreeNode:
    def __init__(self, is_leaf, keys, values, children=None):
        self.is_leaf = is_leaf
        self.keys = keys  # List of keys (sorted)
        self.values = values  # List of corresponding values (same length as keys)
        self.children = children  # List of child node actors (only for non-leaf nodes)


@ray.remote
class DistributedBTree:
    def __init__(self, degree):
        self.degree = degree  # Minimum degree of the BTree
        self.root = None  # Root node actor (initially None)

    def _split_child(self, parent, child_index):
        # Split overloaded child node and update parent
        child = ray.get(child_index.get_node.remote())
        mid_key = child.keys[self.degree - 1]
        mid_value = child.values[self.degree - 1]

        # Create new right child node
        new_child = BTreeNode.remote(
            child.is_leaf, child.keys[self.degree :], child.values[self.degree :]
        )
        if not child.is_leaf:
            new_child.children = ray.put([c for c in child.children[self.degree :]])

        # Update parent keys and children
        parent.keys.insert(child_index, mid_key)
        parent.values.insert(child_index + 1, mid_value)
        parent.children.insert(child_index + 1, new_child)

    def insert(self, key, value):
        ...

    def get(self, key):
        ...


if __name__ == "__main__":
    btree = DistributedBTree.remote(degree=2)  # Create a BTree with minimum degree 2

    ray.get(btree.insert.remote("apple", "red"))
    ray.get(btree.insert.remote("banana", "yellow"))
    ray.get(btree.insert.remote("cherry", "red"))

    value = ray.get(btree.get.remote("apple"))
    print(f"Value for 'apple': {value}")  # Output: Value for 'apple': red
