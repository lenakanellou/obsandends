import math
from collections import deque

class BinarySearchTree:

    # First, a node class is provided, together with essential,
    # useful methods. This is the class that will be used to
    # create the tree and is internal to the BinarySearchTree class.

    class bstNode:
        def __init__(self, val, leftp=None, rightp=None):
            self.val = val
            self.leftp = leftp
            self.rightp = rightp

        def getVal(self):
            return self.val

        def setVal(self, newval):
            self.val = newval

        def leftChild(self):
            return self.leftp

        def rightChild(self):
            return self.rightp

        def setLeftChild(self, newleft):
            self.leftp = newleft

        def setRightChild(self, newright):
            self.rightp = newright

        def __iter__(self):
            if self.leftp != None:
                for node in self.leftp:
                    yield node

            yield self.val

            if self.rightp != None:
                for node in self.rightp:
                    yield node

        def nodeHeight(self):
            if self is None:
                return 0
            else:
                lh = self.leftp.nodeHeight() if self.leftp else 0
                rh 	= self.rightp.nodeHeight() if self.rightp else 0
                return 1 + max(lh, rh)

    # From here on, the methods of the BinarySearchTree class are defined.

    def __init__(self, rootnode=None):
        self.root = rootnode
        self.n = 0

    def treeHeight(self):
        return self.root.nodeHeight()

    def treeBFS(self):

        def __visit_node(node):
            if node == None:
                return None, None
            return node.leftChild(), node.rightChild()

        def __visit_level(level_list):
            next_level_list = []
           # print('Nodes in this level are:')
            for node in level_list:
                # print(node.getVal())
                left, right = __visit_node(node)
                if left != None and left != False:
                    next_level_list.append(left)
                if right != None and right != False:
                    next_level_list.append(right)
            return next_level_list

        level_list = [self.root]
        next_level_list = []
        while level_list != [] :
            print(*(node.getVal() for node in level_list))
            next_level_list = __visit_level(level_list)
            level_list = next_level_list


    def visualize(self):
        levels_visual = [deque(str(self.root.getVal()))]
        next_level_visual = deque(' ' * len(str(self.root.getVal())))
        #levels_visual.append(next_level_visual)
        levels_visual.append(deque())

        level_list = [self.root]
        next_level_list = []
        level = 0

        def __visit_node(node):
            if node == None:
                return None, None
            return node.leftChild(), node.rightChild()


        def __create_level_visual(level_list, level, levels_visual):
            next_level_list = []
            # print(f'Level is {level}, list of levels has {len(levels_visual)} deques')
            if len(levels_visual)-2 < level:
                levels_visual.append(deque())
            #     print(f'New length of list of levels is {len(levels_visual)}')
            # for item in levels_visual:
            #     print(type(item))
            for node in level_list:
                left, right = __visit_node(node)
                if left != None and left != False:
                    next_level_list.append(left)
                    # levels_visual[level+1].appendleft(' ')
                    levels_visual[level+1].append(str(left.getVal()))
                    levels_visual[level+1].append(' ')
                else:
                    levels_visual[level+1].append('X ')

                levels_visual[level+1].append(' ' * len(str(node.getVal())))

                if right != None and right != False:
                    next_level_list.append(right)
                    # levels_visual[level+1].append(' ')
                    levels_visual[level+1].append(str(right.getVal()))
                else:
                    levels_visual[level+1].append(' X')

                levels_visual[level+1].append('  ')

            return next_level_list

        while level_list != [] :
            # print(*(node.getVal() for node in level_list))
            next_level_list = __create_level_visual(level_list, level, levels_visual)
            level_list = next_level_list

            level = level + 1

            for l in range(0, level):
                levels_visual[l].appendleft('  ')

        for row in levels_visual:
            print(*(element for element in row))

    def get_root(self):
        return self.root

    def insert(self, val):

        def __insert(node, val):
            if node == None:
                return BinarySearchTree.bstNode(val)

            # if root.getVal() == val:
            #     return None

            if val < node.getVal():
                node.setLeftChild(__insert(node.leftChild(),val))
            elif val > node.getVal():
                node.setRightChild(__insert(node.rightChild(),val))
            else:
                print(f'value {val} already in tree!')
            return node

        self.root = __insert(self.root, val)


    def search(self, val):

        def __bst_search_rec(node, val):
            if node == None:
                return None
            if node.getVal() == val:
                return node

            if val < node.getVal() :
                node = __bst_search_rec(node.leftp, val)
            else:
                node = __bst_search_rec(node.rightp, val)
            return node

        return __bst_search_rec(self.root, val)

    def delete(self, val):

        def __find_subtree_min(node):
            curr_node = node
            while curr_node.leftChild() is not None:
                curr_node = curr_node.leftChild()
            return curr_node

        def __in_order_successor(node):
            return __find_subtree_min(node.rightChild())


        def __delete(node, val):
            if node is None:
                return None

            if val < node.getVal() :
                node.setLeftChild(__delete(node.leftChild(), val))
            elif val > node.getVal():
                node.setRightChild(__delete(node.rightChild(), val))

            if node.getVal() == val:
            # case study: no child, one child, two children
                if node.leftChild() == None and node.rightChild() == None:
                    return None
                else:
                    if node.leftChild() != None and node.rightChild() == None:
                        return node.leftChild()
                    elif node.leftChild() == None and node.rightChild() != None:
                        return node.rightChild()
                    else:
                        update_val = __in_order_successor(node).getVal()
                        node.setVal(update_val)
                        node.setRightChild(__delete(node.rightChild(), update_val))

            return node

        return __delete(self.root, val)


    def __iter__(self):
        if self.root != None:
            return self.root.__iter__()

        else:
            return [].__iter__()
