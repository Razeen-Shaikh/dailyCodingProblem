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
        print("Starting serialization:", res)

        def dfs(node):
            if not node:
                res.append("#")
            else:
                res.append(node.val)
                dfs(node.left)
                dfs(node.right)

            # Debugging print
            print(f"At Node({node}):", res)

        dfs(root)
        print(f"Serialized output: {','.join(res)}")
        return ",".join(res)

    def deserialize(self, data):
        """Deserialize a string to a binary tree"""
        print(f"Data to deserialize: {data}")
        values = iter(data.split(','))  # Turn string into an iterator for DFS
        print(f"Values iterator: {values}")
        
        def dfs():
            val = next(values)  # Get the next value in the iterator
            print(f"Processing value: {val}")

            if val == '#':  # Base case: If the value is '#', return None
                return None

            node = Node(val)  # Create a new node
            print(f"Created Node({val})")

            # Recursively process left and right children
            node.left = dfs()  # Left child
            print(f"Node({val}) left child: {node.left}")

            node.right = dfs()  # Right child
            print(f"Node({val}) right child: {node.right}")
            
            return node
        
        return dfs()


# Test the implementation
node = Node('root', Node('left', Node('left.left')), Node('right'))
ser = BinaryTree()
deser = BinaryTree()

# Deserialize and check the tree structure
deserialized_root = deser.deserialize("1,2,3,#,#,4,5")
print(deserialized_root.left.left.val == 'left.left')  # Expected: True

# Serialize and then deserialize
serialized = ser.serialize("1,2,3,#,#,4,5")
print(f"Serialized: {serialized}")