class Node:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
    
    def __str__(self):
        # Provide a string representation to print node values clearly
        return f"Node({self.val})"


class BinaryTree:
    """
    Given the root to a binary tree, implement serialize(root), which serializes the tree into a string,
    and deserialize(s), which deserializes the string back into the tree.
    """
    def serialize(self, root):
        res = []

        def dfs(node):
            if not node:
                res.append("#")
            else:
                res.append(node.val)
                dfs(node.left)
                dfs(node.right)

        dfs(root)
        return ",".join(res)

    def deserialize(self, data):
        """Deserialize a string to a binary tree"""
        values = iter(data.split(','))  # Turn string into an iterator for DFS
        
        def dfs():
            val = next(values)  # Get the next value in the iterator

            if val == '#':  # Base case: If the value is '#', return None
                return None

            node = Node(val)  # Create a new node

            # Recursively process left and right children
            node.left = dfs()  # Left child
            node.right = dfs()  # Right child
            
            return node
        
        return dfs()


# Test the implementation
node = Node('root', Node('left', Node('left.left')), Node('right'))
ser = BinaryTree()
deser = BinaryTree()

# Deserialize and check the tree structure
serialized = ser.serialize(node)  # Serialize the node first
deserialized_root = deser.deserialize(serialized)  # Deserialize the serialized string
print(deserialized_root.left.left.val == 'left.left')  # Expected: True

# Serialize and then deserialize
serialized = ser.serialize(node)
print(f"Serialized: {serialized}")