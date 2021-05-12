"""
File: linkedbst.py
Author: Ken Lambert
"""
from math import log
import time
import random
from abstractcollection import AbstractCollection
from bstnode import BSTNode
from linkedstack import LinkedStack


class LinkedBST(AbstractCollection):
    """An link-based binary search tree implementation."""

    def __init__(self, sourceCollection=None):
        """Sets the initial state of self, which includes the
        contents of sourceCollection, if it's present."""
        self._root = None
        AbstractCollection.__init__(self, sourceCollection)

    # Accessor methods
    def __str__(self):
        """Returns a string representation with the tree rotated
        90 degrees counterclockwise."""

        def recurse(node, level):
            sline = ""
            if node is not None:
                sline += recurse(node.right, level + 1)
                sline += "| " * level
                sline += str(node.data) + "\n"
                sline += recurse(node.left, level + 1)
            return sline

        return recurse(self._root, 0)

    def __iter__(self):
        """Supports a preorder traversal on a view of self."""
        if not self.isEmpty():
            stack = LinkedStack()
            stack.push(self._root)
            while not stack.isEmpty():
                node = stack.pop()
                yield node.data
                if node.right is not None:
                    stack.push(node.right)
                if node.left is not None:
                    stack.push(node.left)

    def preorder(self):
        """Supports a preorder traversal on a view of self."""
        return None

    def inorder(self):
        """Supports an inorder traversal on a view of self."""
        lyst = list()

        def recurse(node):
            if node is not None:
                recurse(node.left)
                lyst.append(node.data)
                recurse(node.right)

        recurse(self._root)
        return iter(lyst)

    def postorder(self):
        """Supports a postorder traversal on a view of self."""
        return None

    def levelorder(self):
        """Supports a levelorder traversal on a view of self."""
        return None

    def __contains__(self, item):
        """Returns True if target is found or False otherwise."""
        return self.find(item) is not None

    def find(self, item):
        """If item matches an item in self, returns the
        matched item, or None otherwise."""

        def recurse(node):
            if node is None:
                return None
            elif item == node.data:
                return node.data
            elif item < node.data:
                return recurse(node.left)
            else:
                return recurse(node.right)

        return recurse(self._root)

    # Mutator methods
    def clear(self):
        """Makes self become empty."""
        self._root = None
        self._size = 0

    def add(self, item):
        """Adds item to the tree."""

        # Helper function to search for item's position
        def recurse(node):
            # New item is less, go left until spot is found
            if item < node.data:
                if node.left == None:
                    node.left = BSTNode(item)
                else:
                    recurse(node.left)
            # New item is greater or equal,
            # go right until spot is found
            elif node.right == None:
                node.right = BSTNode(item)
            else:
                recurse(node.right)
                # End of recurse

        # Tree is empty, so new item goes at the root
        if self.isEmpty():
            self._root = BSTNode(item)
        # Otherwise, search for the item's spot
        else:
            recurse(self._root)
        self._size += 1

    def remove(self, item):
        """Precondition: item is in self.
        Raises: KeyError if item is not in self.
        postcondition: item is removed from self."""
        if not item in self:
            raise KeyError("Item not in tree.""")

        # Helper function to adjust placement of an item
        def lift_max_in_left_subtree_to_top(top):
            # Replace top's datum with the maximum datum in the left subtree
            # Pre:  top has a left child
            # Post: the maximum node in top's left subtree
            #       has been removed
            # Post: top.data = maximum value in top's left subtree
            parent = top
            current_node = top.left
            while not current_node.right == None:
                parent = current_node
                current_node = current_node.right
            top.data = current_node.data
            if parent == top:
                top.left = current_node.left
            else:
                parent.right = current_node.left

        # Begin main part of the method
        if self.isEmpty(): return None

        # Attempt to locate the node containing the item
        item_removed = None
        pre_root = BSTNode(None)
        pre_root.left = self._root
        parent = pre_root
        direction = 'L'
        current_node = self._root
        while not current_node == None:
            if current_node.data == item:
                item_removed = current_node.data
                break
            parent = current_node
            if current_node.data > item:
                direction = 'L'
                current_node = current_node.left
            else:
                direction = 'R'
                current_node = current_node.right

        # Return None if the item is absent
        if item_removed == None: return None

        # The item is present, so remove its node

        # Case 1: The node has a left and a right child
        #         Replace the node's value with the maximum value in the
        #         left subtree
        #         Delete the maximium node in the left subtree
        if not current_node.left == None \
                and not current_node.right == None:
            lift_max_in_left_subtree_to_top(current_node)
        else:

            # Case 2: The node has no left child
            if current_node.left == None:
                new_child = current_node.right

                # Case 3: The node has no right child
            else:
                new_child = current_node.left

                # Case 2 & 3: Tie the parent to the new child
            if direction == 'L':
                parent.left = new_child
            else:
                parent.right = new_child

        # All cases: Reset the root (if it hasn't changed no harm done)
        #            Decrement the collection's size counter
        #            Return the item
        self._size -= 1
        if self.isEmpty():
            self._root = None
        else:
            self._root = pre_root.left
        return item_removed

    def height(self):
        '''
        Return the height of tree
        :return: int
        '''
        def height1(top):
            '''
            Helper function
            :param top:
            :return:
            '''
            if top is None:
                return -1
            else:
                return 1 + max(height1(top.left), height1(top.right))
        return height1(self._root)

    def is_balanced(self):
        '''
        Return True if tree is balanced
        :return:
        '''
        return self.height() <= 2 * log(self._size + 1,2) - 1

    def replace(self, item, new_item):
        """
        If item is in self, replaces it with new_item and
        returns the old item, or returns None otherwise."""
        probe = self._root
        while probe != None:
            if probe.data == item:
                olddata = probe.data
                probe.data = new_item
                return olddata
            elif probe.data > item:
                probe = probe.left
            else:
                probe = probe.right
        return None


    def range_find(self, low, high):
        '''
        Returns a list of the items in the tree, where low <= item <= high."""
        :param low:
        :param high:
        :return:
        '''
        find_list, nodes = [], self.inorder()
        for node in nodes:
            if low<=node<=high:
                find_list.append(node)
        return find_list

    def rebalance(self):
        '''
        Rebalances the tree.
        :return:
        '''
        notbalanced = list(self.inorder())
        self.clear()

        def balance_recurse(tree):
            if not tree:
                return None

            node = BSTNode(tree[len(tree) // 2])
            node.right = balance_recurse(tree[len(tree) // 2 + 1:])
            node.left = balance_recurse(tree[:len(tree) // 2])

            return node

        self._root = balance_recurse(notbalanced)

    def successor(self, item):
        """
        Returns the smallest item that is larger than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        nodes = list(self.inorder())
        for node in nodes:
            if node > item:
                return node
        return None

    def predecessor(self, item):
        """
        Returns the largest item that is smaller than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        lst = []
        nodes = list(self.inorder())
        for node in nodes:
            if node < item:
                lst.append(node)
        if lst:
            return lst[-1]
        return None

    def read_file(self, filename, random_indexes):
        """
        (str, list) -> str, list

        Function reads the file and returns random words from that
        """

        file = open(filename , 'r' )
        contents, result = file.read().split('\n'), []

        for num in random_indexes:
            result.append(contents[num])

        return contents, result

    def lookup_list(self, lst_words, rnd_words):
        """
        (list, list) -> double

        Function meausures the time that is needed for
        looking words up using the list.
        """
        start, counter_of_word = time.time(), 0

        for word in lst_words:
            if word in rnd_words:
                counter_of_word +=1
        return time.time() - start

    def lookup_sorted_dict(self, rnd_words):
        '''
        (list, list) -> double

        Function meausures the time that is needed for
        looking words up using the binary tree(alphabet-sorted).
        '''
        tree, restricted_words = LinkedBST(), rnd_words[:900]
        for word in restricted_words:
            tree.add(word)

        start = time.time()

        for _ in range(10001):
            random_idx = random.randint(0, 899)
            tree.find(rnd_words[random_idx])
        return time.time() - start

    def lookup_unsorted_dict(self, rnd_words):
        '''
        (list, list) -> double

        Function meausures the time that is needed for
        looking words up using the binary tree(alphabet-unsorted).
        '''
        tree, mixed_words = LinkedBST(), list(set(rnd_words))[:900]
        for word in mixed_words:
            tree.add(word)

        start = time.time()

        for _ in range(10001):
            random_idx = random.randint(0, 899)
            tree.find(mixed_words[random_idx])
        return time.time() - start

    def lookup_balance(self, rnd_words):
        '''
        (list, list) -> double

        Function meausures the time that is needed for
        looking words up using the balanced binary tree.
        '''
        tree, mixed_words = LinkedBST(), list(set(rnd_words))[:900]
        for word in mixed_words:
            tree.add(word)

        tree.rebalance()
        start = time.time()

        for _ in range(10001):
            random_idx = random.randint(0, 899)
            tree.find(mixed_words[random_idx])
        return time.time() - start

    def demo_bst(self, path):
        """
        Demonstration of efficiency binary search tree for the search tasks.
        :param path:
        :type path:
        :return:
        :rtype:
        """
        random_indexes = []
        while len(random_indexes) != 10000:
            index = random.randint(0, 10001)
            if index not in random_indexes:
                random_indexes.append(index)
        random_indexes.sort()

        words, random_words = self.read_file(path, random_indexes)

        lookup_time_list = round(self.lookup_list(words, random_words), 4)
        lookup_time_sorted = round(self.lookup_sorted_dict(random_words), 4)
        lookup_time_unsorted = round(self.lookup_unsorted_dict(random_words), 4)
        lookup_time_balance = round(self.lookup_balance(random_words), 4)
        print("=========================================")
        print("List look-up took " + str(lookup_time_list) + " seconds")
        print("Sorted tree look-up took " + str(lookup_time_sorted) + " seconds")
        print("Unsorted tree look-up took " + str(lookup_time_unsorted) + " seconds")
        print("Balance tree look-up took " + str(lookup_time_balance) + " seconds")
        print("=========================================")



if __name__ == "__main__":
    bst = LinkedBST()
    bst.demo_bst("words.txt")
