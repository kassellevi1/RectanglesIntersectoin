from enum import Enum

################################################################################################################################################################################
#                                           N RECTANGLES INTERSECTION PROBLEM - DL&CV Student assignments                                                                      #
#               This problem can be solve easily with a O(N^2) naive solution (checking intersection between all pairwise rectangle)                                           #
#                for efficiency and complexity reduction i decided to solve this with the 'SWEEP LINE' algorithm (https://en.wikipedia.org/wiki/Sweep_line_algorithm)          #
#                       for more details refer to this article : "Algorithms for Reporting and Counting Geometric Intersections" by Bentley et al.                             #
################################################################################################################################################################################


def count_intersections(input_file_path):
    """"
    This function creates the “rectangles_count.txt” file which is identical to the input file, but with an additional
    value at the end of each line - the number of intersections of that rectangle.
    :param:  input_file_path: The path to the input file containing list of N rectangles.
    """
    rectangles, sorted_segment_list = parse_input(input_file_path)
    BinIntervalTree = RedBlackTree()  # Interval binary search self-balance tree (Red-Black-Tree)
    BinIntervalTree.insert(sorted_segment_list[0])  # insert the first node
    BinIntervalTree.construct_max()  # after each insertion - reconstructing the max of each node
    for segment in sorted_segment_list[1:]:
        """
        Sweep line algorithm - from left to right.
        left segment - insertion
        right segment - deletion 
        """
        if segment.Side == Segment.Side.Left:
            """
            for each left segments we perform 3 operation
                1. check which intersections have the corresponding rectangle
                2. insert the segment to the RedBlackTree
                3. reconstruct the mac label of the interval Tree
            """
            BinIntervalTree.search_interval_intersections(BinIntervalTree.root, segment)
            BinIntervalTree.insert(segment)
            BinIntervalTree.construct_max()
        elif segment.Side == Segment.Side.Right:
            """"
            for each right segments we delete the segment and reconstruct the max labels
            """
            BinIntervalTree.delete_node(segment)
            BinIntervalTree.construct_max()
        else:
            raise Exception("The segment is invalid")

    write_output_file(rectangles, 'rectangles_count.txt')

def parse_input(input_file_path):
    """
    Parsing 'rectangles.txt' to rectangles objects and extract their segments.
    :param input_file_path: The path to the input file containing list of N rectangles.
    :return: list of N rectangles objects, sorted list of all vertical segments
    """
    with open(input_file_path, "r") as f:
        lines = f.readlines()
    rectangles = []
    segment_list = []
    for line in lines:
        rect_arg = line.split(' ')
        rectangle = Rectangle(int(rect_arg[0]), int(rect_arg[1]), int(rect_arg[2]), int(rect_arg[3]))
        rectangles.append(rectangle)

        left_segment = Segment(rectangle.x_left, rectangle.vertical_segment, rectangle, Segment.Side.Left)
        right_segment = Segment(rectangle.x_right, rectangle.vertical_segment, rectangle, Segment.Side.Right)

        segment_list.append(left_segment)
        segment_list.append(right_segment)

    sorted_segment_list = sorted(segment_list, key=lambda segment: segment.x_cor)  # sort the segments list by the x coordinate

    return rectangles, sorted_segment_list


def write_output_file(rectangles_list, output_file_name):
    """
    This function create the desired output file
    :param rectangles_list: the list of rectangles objects
    :param output_file_name: the name of the output file
    """
    f = open(output_file_name, 'w')
    for rectangle in rectangles_list:
        str = '{} {} {} {} {}\n'.format(rectangle.x_left, rectangle.y, rectangle.dx, rectangle.dy,
                                    rectangle.num_of_intersection)
        f.write(str)
    f.close()


class Segment:

    def __init__(self, x_cor, vert_segment, rectangle, side):
        """
        :x_cor: the x coordinate of the vertical segment
        :vert_segment: the vertical segment
        :rectangle: the corresponding rectangle of the segment
        :side: the corresponding side of the vertical segment (Left/Right)
        """
        self.x_cor = x_cor
        self.vert_segment = vert_segment
        self.rectangle = rectangle
        self.Side = side

    class Side(Enum):
        Left = 1
        Right = 2


class Rectangle:

    def __init__(self, x, y, dx, dy):
        """
        :x_left: the left x coordinate
        :x_right: the right x coordinate
        :vertical_segment: the vertical segment of the rectangle
        :num_of_intersection : the total number of intersections with other rectangles
        """
        self.x_left = x
        self.x_right = x + dx
        self.y = y
        self.dx = dx
        self.dy = dy
        self.vertical_segment = [y - dy, y]
        self.num_of_intersection = 0

    def add_intersection(self):
        self.num_of_intersection += 1


class Node:
    def __init__(self, segment=None):
        """
        :rectangle: the rectangle corresponding to the node
        :interval:
        :data: data is the 'key' of the BST. the key is the left coordinate of the interval
        :parent: pointer to the parent
        :left: pointer to left child
        :right: pointer to right child
        :color: 1 . Red, 0 . Black
        :Max: hold the Max right side interval of his subtree
        """
        self.rectangle = segment.rectangle
        self.interval = segment.vert_segment
        self.data = segment.vert_segment[0]
        self.parent = None
        self.left = None
        self.right = None
        self.color = 1
        self.Max = None

    def has_child(self):
        if self.left or self.right:
            return True
        return False


class RedBlackTree:
    def __init__(self):
        """
        :root: the root of the tree
        """
        self.TNULL = Node(Segment(0, (0, 0), Rectangle(0, 0, 0, 0), Segment.Side.Left))  # Nil leave initialization
        self.TNULL.color = 0
        self.TNULL.left = None
        self.TNULL.right = None
        self.root = self.TNULL

    def search_interval_intersections(self, root, segment):
        """
        This function find all the intersections between the sub tree (starting at 'root') and the query interval in
        a recursive way The function return a list of all the intersections of the interval with the RedBlackTree
        :param root: the root of the subtree :param segment: the query segment
        """
        if root:
            if self.is_intersecting(root.interval, segment.vert_segment):  # if the root is root Null
                root.rectangle.add_intersection()
                segment.rectangle.add_intersection()

            if root.left != None and root.left.Max >= segment.vert_segment[0]:  # if the is a left child AND the
                # left child Max is bigger then the left side interval - a potential interval intersection
                self.search_interval_intersections(root.left, segment)  # check all the intersection of the left sub tree

            self.search_interval_intersections(root.right, segment)  # check all the intersection of the right sub tree

        return

    def is_intersecting(self, interval_left, interval_right):
        """
        This function check if there is an intersection between 2 intervals
        :param interval_left: the left query interval
        :param interval_right: the right query interval
        :return: True if there is an intersection between the two interval and False if not
        """
        if interval_left == (0, 0):  # Nil leave
            return False
        if (interval_left[0] > interval_right[1]) or (interval_left[1] < interval_right[0]):  # no intersection
            return False

        return True

    def max_of_sub_tree(self, root_node):
        """
        This function return the Max interval between his 2 child sub trees and his own in a recursive way
        :param root_node: the root of the subtree
        :return: Max interval between his 2 child sub trees and his own in a recursive way
        """
        if root_node.has_child():
            max_array = []
            if root_node.left:
                self.max_of_sub_tree(root_node.left)
                max_array.append(root_node.left.Max)
            if root_node.right:
                self.max_of_sub_tree(root_node.right)
                max_array.append(root_node.right.Max)
            max_array.append(root_node.interval[1])
            root_node.Max = max(max_array)
            return

        else:
            root_node.Max = root_node.interval[1]
            return

    def construct_max(self):
        """
        This function construct the Max label of each node
        :return:
        """
        node = self.root
        self.max_of_sub_tree(node)

    def search_tree_helper(self, node, key):
        """
        This function find the node corresponding to the key
        :param node: the suggested node
        :param key: the key that we are searching
        :return:
        """
        if node == self.TNULL or key == node.data:
            return node

        if key < node.data:
            return self.search_tree_helper(node.left, key)
        return self.search_tree_helper(node.right, key)

    def fix_delete(self, x):
        """
        This function fix the RedBlackTree that was modified by the delete operation
        :param x: the node that need to be fixed
        """
        while x != self.root and x.color == 0:
            if x == x.parent.left:  # if x is the left child of his parent
                s = x.parent.right
                if s.color == 1:
                    s.color = 0  # case 3.1  x ’s sibling S is red
                    x.parent.color = 1
                    self.left_rotate(x.parent)
                    s = x.parent.right

                if s.left.color == 0 and s.right.color == 0:
                    s.color = 1  # case 3.2   x’s sibling S is black, and both of S’s children are black.
                    x = x.parent
                else:
                    if s.right.color == 0:
                        s.left.color = 0  # case 3.3  x ’s sibling S is black, S’s left child is red, and S’s right child is black.
                        s.color = 1
                        self.right_rotate(s)
                        s = x.parent.right

                    s.color = x.parent.color  # case 3.4  x’s sibling S is black, and S’s right child is red.
                    x.parent.color = 0
                    s.right.color = 0
                    self.left_rotate(x.parent)
                    x = self.root
            else:  # if x is the left child of his parent
                s = x.parent.left
                if s.color == 1:
                    s.color = 0  # case 3.1  x ’s sibling S is red
                    x.parent.color = 1
                    self.right_rotate(x.parent)
                    s = x.parent.left

                if s.left.color == 0 and s.right.color == 0:
                    s.color = 1  # case 3.2   x’s sibling S is black, and both of S’s children are black.
                    x = x.parent
                else:
                    if s.left.color == 0:  # case 3.3  x ’s sibling S is black, S’s left child is red, and S’s right child is black.
                        s.right.color = 0
                        s.color = 1
                        self.left_rotate(s)
                        s = x.parent.left

                    s.color = x.parent.color  # case 3.4  x’s sibling S is black, and S’s right child is red.
                    x.parent.color = 0
                    s.left.color = 0
                    self.right_rotate(x.parent)
                    x = self.root
        x.color = 0

    def rb_transplant(self, u, v):
        if u.parent is None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    def delete_node_helper(self, node, key):
        """
        This function find the node containing key
        :param node: the node that is the root of the subtree
        :param key: the desired key that need to be deleted
        """
        z = self.TNULL
        while node != self.TNULL:
            if node.data == key:
                z = node
            if node.data <= key:
                node = node.right
            else:
                node = node.left
        if z == self.TNULL:
            print("Couldn't find key in the tree")
            return
        y = z
        y_original_color = y.color
        if z.left == self.TNULL:
            x = z.right
            self.rb_transplant(z, z.right)
        elif z.right == self.TNULL:
            x = z.left
            self.rb_transplant(z, z.left)
        else:
            y = self.minimum(z.right)
            y_original_color = y.color
            x = y.right
            if y.parent == z:
                x.parent = y
            else:
                self.rb_transplant(y, y.right)
                y.right = z.right
                y.right.parent = y

            self.rb_transplant(z, y)
            y.left = z.left
            y.left.parent = y
            y.color = z.color
        if y_original_color == 0:
            self.fix_delete(x)

    def fix_insert(self, k):
        """
        This function fix the RedBlackTree that was modified by the insert operation
        :param k: the node that we want to fix
        """

        while k.parent.color == 1:
            if k.parent == k.parent.parent.right:
                u = k.parent.parent.left  # e.g. the uncle
                if u.color == 1:  # case 3.1  P is red and U is red too.
                    u.color = 0
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    k = k.parent.parent
                else:
                    if k == k.parent.left:  # case 3.2.2  P is right child of G and K is left child of P.
                        k = k.parent
                        self.right_rotate(k)
                    k.parent.color = 0  # case 3.2.1  P is right child of G and K is right child of P.
                    k.parent.parent.color = 1
                    self.left_rotate(k.parent.parent)
            else:
                u = k.parent.parent.right  # e.g. the uncle

                if u.color == 1:  # mirror case 3.1  P  is red and U is red too.
                    u.color = 0
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    k = k.parent.parent
                else:
                    if k == k.parent.right:  # mirror case 3.2.2 P is right child of G and K is left child of P.
                        k = k.parent
                        self.left_rotate(k)  # mirror case 3.2.1 P is right child of G and K is right child of P.
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    self.right_rotate(k.parent.parent)
            if k == self.root:
                break
        self.root.color = 0

    def minimum(self, node):
        """
        This function find the node with the minimum key
        :param node: the node that we want to find the node with the minimum key below him
        :return: the minimum node with the minimum key
        """
        while node.left != self.TNULL:
            node = node.left
        return node

    def maximum(self, node):
        """
        This function find the node with the minimum key
        :param node: the node that we want to find the node with the maximum key below him
        :return: the minimum node with the minimum key
        """
        # This function find the node with the minimum key
        while node.right != self.TNULL:
            node = node.right
        return node

    def successor(self, x):
        """
        This function find the successor of a given node
        :param x: the node that we want to find the successor node below him
        :return: the successor node
        """
        if x.right != self.TNULL:  # if the right subtree is not None,the successor is the leftmost node in the right subtree
            return self.minimum(x.right)

        y = x.parent  # else it is the lowest ancestor of x whose left child is also an ancestor of x.
        while y != self.TNULL and x == y.right:
            x = y
            y = y.parent
        return y

    def predecessor(self, x):
        """
        This function find the predecessor of a given node
        :param x: the node that we want to find the predecessor node below him
        :return: the predecessor node
        """
        if x.left != self.TNULL:  # if the left subtree is not None, the predecessor is the rightmost node in the left subtree
            return self.maximum(x.left)

        y = x.parent
        while y != self.TNULL and x == y.left:
            x = y
            y = y.parent
        return y

    def left_rotate(self, x):
        """
        This function perform a left rotation  at node x
        :param x: the node that we perform the left rotation on him
        """
        y = x.right
        x.right = y.left
        if y.left != self.TNULL:
            y.left.parent = x

        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    # rotate right at node x
    def right_rotate(self, x):
        """
        This function perform a right rotation  at node x
        :param x: the node that we perform the right rotation on him
        """
        y = x.left
        x.left = y.right
        if y.right != self.TNULL:
            y.right.parent = x

        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y

    def insert(self, segment):
        """
        This function insert the segment key to the tree in its appropriate position with Ordinary Binary Search Insertion
        :param segment: the segment that we want to insert to the RedBlackTree
        """
        node = Node(segment)
        node.parent = None
        node.data = segment.vert_segment[0]
        node.left = self.TNULL
        node.right = self.TNULL
        node.color = 1  # new node must be red
        y = None
        x = self.root

        while x != self.TNULL:
            y = x
            if node.data < x.data:
                x = x.left
            else:
                x = x.right

        node.parent = y  # y is parent of x
        if y is None:
            self.root = node
        elif node.data < y.data:
            y.left = node
        else:
            y.right = node

        if node.parent is None:  # if new node is a root node, simply return
            node.color = 0
            return

        if node.parent.parent is None:  # if the grandparent is None, simply return
            return

        self.fix_insert(node)  # Fix the tree such that it will be a RedBlackTree

    def delete_node(self, segment):
        """
        This function delete the node from the tree
        :param segment: the segment that we want to remove from the RedBlackTree
        """
        self.delete_node_helper(self.root, segment.vert_segment[0])


if __name__ == '__main__':

    count_intersections(input_file_path='rectangles.txt')
