class Node:
    def __init__(self,patient):
        self.patient = patient
        self.left = None
        self.right = None

class BST:
    def __init__(self):
        self.root = None

    def insert(self,patient):
        self.root = self._insert_recursive(self.root,patient)

    def _insert_recursive(self,node,patient):
        if not node:
            return Node(patient)
        if patient.name < node.patient.name:
            node.left=self._insert_recursive(node.left,patient)
        else:
            node.right = self._insert_recursive(node.roght,patient)
        return node

    def inorder_traversal(self):
        return self._inorder(self.root)
    def _inorder(self,node):
        if not node:
            return []
        return self._inorder(node.left)+[node.patient]+ self._inorder(node.right)

    def search(self,name):
        return self._search_recursive(self.root,name)

    def _search_recursive(self,node,name):
        if not node:
            return None
        if name == node.patient.name:
            return node.patient
        elif name < node.patient.name:
            return self._search_recursive(node.left,name)
        else:
            return self._search_recursive(node.right,name)
