
class Rectangle:

    def __init__(self, x, y, dx, dy):
        self.x_left = x                         #the left x coordinate of the rectangle.
        self.x_right = x + dx                   #the right x coordinate of the rectangle.  the sweep algorithm will sorted acording to them
        self.y = y
        self.dx = dx
        self.dy = dy
        self.vertical_segment = [y-dy,y]        #the vertical segment of the rectangle - neccessery for line sweep search
        self.num_of_intersection = 0            #counting the number of pairwise intrsections with these rectangle

    def add_intersection(self):
        self.num_of_intersection += 1

class Node():
    def __init__(self, interval = None,index = None):
        self.index = index                      #the index of the rectangle corrospending to the node
        self.interval = interval
        self.data = interval[0]                 #data is the 'key' of the BST. the key is the left cordinate of the interval
        self.parent = None                      #pointer to the parent
        self.left = None                        #pointer to left child
        self.right = None                       #pointer to right child
        self.color = 1                          # 1 . Red, 0 . Black
        self.Max = None                         # hold the Max right side interval of his subtree

    def has_child(self):
        if self.left or self.right:
            return True
        return False



class RedBlackTree():
    def __init__(self):
        self.TNULL = Node((0,0))                #Nil leave initionalization
        self.TNULL.color = 0
        self.TNULL.left = None
        self.TNULL.right = None
        self.root = self.TNULL

    def search_interval_intersections(self, root, query_interval,base_index,rectangels_list):
        ## This function find all the intersectoins between the sub tree (starting at 'root') and the query interval in a recursive way
        ## The function return a list of all the intersections of the interval with the RedBlackTree

        if (root):
            if (self.is_intersecting(root.interval, query_interval)):                            #if the root is noot Null
                rectangels_list[root.index].add_intersection()
                rectangels_list[base_index].add_intersection()


            if (root.left != None and root.left.Max >= query_interval[0]):                       #if the is a left child AND the left child Max is bigger then the left sude interval - a potintioal interval intersction
                self.search_interval_intersections(root.left,query_interval,base_index,rectangels_list)    #check all the intersection of the left sub tree

            self.search_interval_intersections(root.right,query_interval,base_index,rectangels_list)      #check all the intersection of the right sub tree

        return

    def is_intersecting(self, interval_left, interval_right):
        ##This function check if there is an intersction between 2 intervals
        if interval_left == (0,0):                                                               #Nil leave
            return False
        if ((interval_left[0] > interval_right[1]) or (interval_left[1] < interval_right[0])):   #no intersectoin
            return False

        return True

    def max_of_sub_tree(self, root_node):
        ## This function return the Max interval between his 2 child sub trees and his own in a recutsive way
        if ((root_node.has_child())):
            max_array = []
            if (root_node.left):
                self.max_of_sub_tree(root_node.left)
                max_array.append(root_node.left.Max)
            if (root_node.right):
                self.max_of_sub_tree(root_node.right)
                max_array.append(root_node.right.Max)
            max_array.append(root_node.interval[1])
            root_node.Max = max(max_array)
            return

        else:
            root_node.Max = root_node.interval[1]
            return

    def construct_max(self):
        ## This function constuct the Max label of each node
        node = self.root
        self.max_of_sub_tree(node)

    def search_tree_helper(self, node, key):
        ## This function find the node corerespondinf to the key
        if node == self.TNULL or key == node.data:
            return node

        if key < node.data:
            return self.search_tree_helper(node.left, key)
        return self.search_tree_helper(node.right, key)


    def fix_delete(self, x):
        ## This functoin fix the RedBlackTree that was modified by the delete operation
        while x != self.root and x.color == 0:
            if x == x.parent.left:                          # if x is the left child of his parent
                s = x.parent.right
                if s.color == 1:
                    s.color = 0                             # case 3.1  x ’s sibling S is red
                    x.parent.color = 1
                    self.left_rotate(x.parent)
                    s = x.parent.right

                if s.left.color == 0 and s.right.color == 0:
                    s.color = 1                             # case 3.2   x’s sibling S is black, and both of S’s children are black.
                    x = x.parent
                else:
                    if s.right.color == 0:
                        s.left.color = 0                    # case 3.3  x ’s sibling S is black, S’s left child is red, and S’s right child is black.
                        s.color = 1
                        self.right_rotate(s)
                        s = x.parent.right

                    s.color = x.parent.color                # case 3.4  x’s sibling S is black, and S’s right child is red.
                    x.parent.color = 0
                    s.right.color = 0
                    self.left_rotate(x.parent)
                    x = self.root
            else:                                           # if x is the left child of his parent
                s = x.parent.left
                if s.color == 1:
                    s.color = 0                             # case 3.1  x ’s sibling S is red
                    x.parent.color = 1
                    self.right_rotate(x.parent)
                    s = x.parent.left

                if s.left.color == 0 and s.right.color == 0:
                    s.color = 1                             # case 3.2   x’s sibling S is black, and both of S’s children are black.
                    x = x.parent
                else:
                    if s.left.color == 0:                   # case 3.3  x ’s sibling S is black, S’s left child is red, and S’s right child is black.
                        s.right.color = 0
                        s.color = 1
                        self.left_rotate(s)
                        s = x.parent.left

                    s.color = x.parent.color                # case 3.4  x’s sibling S is black, and S’s right child is red.
                    x.parent.color = 0
                    s.left.color = 0
                    self.right_rotate(x.parent)
                    x = self.root
        x.color = 0

    def rb_transplant(self, u, v):
        if u.parent == None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    def delete_node_helper(self, node, key):
        ## This function find the node containing key
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
        elif (z.right == self.TNULL):
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
        ## This functoin fix the RedBlackTree that was modified by the insert operation
        while k.parent.color == 1:
            if k.parent == k.parent.parent.right:
                u = k.parent.parent.left                # e.g. the uncle
                if u.color == 1:                        # case 3.1  P is red and U is red too.
                    u.color = 0
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    k = k.parent.parent
                else:
                    if k == k.parent.left:              # case 3.2.2  P is right child of G and K is left child of P.
                        k = k.parent
                        self.right_rotate(k)
                    k.parent.color = 0                  # case 3.2.1  P is right child of G and K is right child of P.
                    k.parent.parent.color = 1
                    self.left_rotate(k.parent.parent)
            else:
                u = k.parent.parent.right               # e.g. the uncle

                if u.color == 1:                        # mirror case 3.1  P  is red and U is red too.
                    u.color = 0
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    k = k.parent.parent
                else:
                    if k == k.parent.right:             # mirror case 3.2.2 P is right child of G and K is left child of P.
                        k = k.parent
                        self.left_rotate(k)             # mirror case 3.2.1 P is right child of G and K is right child of P.
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    self.right_rotate(k.parent.parent)
            if k == self.root:
                break
        self.root.color = 0

    def minimum(self, node):
        ## This function find the node with the minimum key
        while node.left != self.TNULL:
            node = node.left
        return node

    def maximum(self, node):
        ## This function find the node with the minimum key
        while node.right != self.TNULL:
            node = node.right
        return node


    def successor(self, x):
        ## This function find the successor of a given node

        if x.right != self.TNULL:                           # if the right subtree is not None,the successor is the leftmost node in the right subtree
            return self.minimum(x.right)


        y = x.parent                                        # else it is the lowest ancestor of x whose left child is also an ancestor of x.
        while y != self.TNULL and x == y.right:
            x = y
            y = y.parent
        return y


    def predecessor(self, x):
        ## This function find the predecessor of a given node

        if (x.left != self.TNULL):              #if the left subtree is not None, the predecessor is the rightmost node in the left subtree
            return self.maximum(x.left)

        y = x.parent
        while y != self.TNULL and x == y.left:
            x = y
            y = y.parent
        return y


    def left_rotate(self, x):
        ## This function perform a left rotation  at node x
        y = x.right
        x.right = y.left
        if y.left != self.TNULL:
            y.left.parent = x

        y.parent = x.parent
        if x.parent == None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    # rotate right at node x
    def right_rotate(self, x):
        ## This function perform a right rotation  at node x
        y = x.left
        x.left = y.right
        if y.right != self.TNULL:
            y.right.parent = x

        y.parent = x.parent
        if x.parent == None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y



    def insert(self, interval,index):
        ## This function insert the key to the tree in its appropriate position
        ## with Ordinary Binary Search Insertion
        node = Node(interval,index)
        node.parent = None
        node.data = interval[0]
        node.left = self.TNULL
        node.right = self.TNULL
        node.color = 1                          # new node must be red

        y = None
        x = self.root

        while x != self.TNULL:
            y = x
            if node.data < x.data:
                x = x.left
            else:
                x = x.right

        node.parent = y                         # y is parent of x
        if y == None:
            self.root = node
        elif node.data < y.data:
            y.left = node
        else:
            y.right = node

        if node.parent == None:                 # if new node is a root node, simply return
            node.color = 0
            return

        if node.parent.parent == None:          # if the grandparent is None, simply return
            return

        self.fix_insert(node)                   # Fix the tree such that it will be a RedBlackTree


    def delete_node(self, data):
        ## This function delete the node from the tree
        self.delete_node_helper(self.root, data)

def write_output_file(rectangles_list,output_file_name):
    ## This function writes the output fils
    f = open(output_file_name,'w')
    for rectagle in rectangles_list:
        str = '{} {} {} {} {}\n'.format(rectagle.x_left,rectagle.y,rectagle.dx,rectagle.dy,rectagle.num_of_intersection)
        f.write(str)
    f.close()


################################################################################################################################################################################
#                                            N RECTANGLES INTERSECTION PROBLEM - DL&CV Student assinments                                                                      #
#                This problem can be solve easily with a O(N^2) naive solution (checking intersecton between all pairwise rectangle)                                           #
#                for efficiency and comlecsity resuction a choosed to solve this with the 'SWEEP LINE' algorithm (https://en.wikipedia.org/wiki/Sweep_line_algorithm)          #
#                       for more details refer to this article : "Algorithms for Reporting and Counting Geometric Intersections" by Bentely et al.                             #
################################################################################################################################################################################
if __name__ == '__main__':
    f = open('rectangles.txt', "r")
    rectangles = []                                                  #list of all rectangles object
    segment_list = []                                                #list of all right and left vertical segments

    for index,x in enumerate(f):
        ## parsing 'rectangles.txt' to rectangles objects and extract there segments
        ## every segment represent by a 4 value dictionary.
        ## 'x_cor' : the x coordinate of the vertical segment
        ## 'vert_segment' : the vertical segment
        ## 'index' : the corresponding index of the rectangle
        ## 'side' : the corresponding side of the vertical segment (Left/Right)
        rect_arg = x.split(' ')
        rectangles.append(Rectangle(int(rect_arg[0]),int(rect_arg[1]),int(rect_arg[2]),int(rect_arg[3])))
        segment_left = {'x_cor': rectangles[index].x_left,"vert_segment": rectangles[index].vertical_segment,"index": index,"side": 'left'}
        segment_right = {"x_cor": rectangles[index].x_right,"vert_segment": rectangles[index].vertical_segment,"index": index,"side": 'right'}

        segment_list.append(segment_left)
        segment_list.append(segment_right)


    sorted_segment_list = sorted(segment_list,key=lambda segment: segment['x_cor'])                         #sort the segments list by the x cordinate
    start1 = timer()
    BinIntervalTree = RedBlackTree()                                                                        #Interval binary search self-balance tree (Red-Black-Tree)
    BinIntervalTree.insert(sorted_segment_list[0]['vert_segment'],sorted_segment_list[0]['index'])          #insert the first node
    BinIntervalTree.construct_max()                                                                         #after each insertion - recunstructing the max of each node
    for ind,segment in enumerate(sorted_segment_list[1:]):
        ## sweep line algorithm - from left to right.
        ## left segment - insertion
        ## right segment - deletion

        if segment['side'] == 'left':
            ## for each left segments we perform 3 operation
            ## 1. check which intersections have the corresponding rectangle
            ## 2. insert the segment to the RedBlackTree
            ## 3. reconstruct the mac label of the interval Tree
            BinIntervalTree.search_interval_intersections(BinIntervalTree.root,segment['vert_segment'],segment['index'],rectangles)
            BinIntervalTree.insert(segment['vert_segment'],segment['index'])
            BinIntervalTree.construct_max()
        elif segment['side'] == 'right':
            ## for each right segments we delete the segment and reconstruct the max label
            BinIntervalTree.delete_node(segment['vert_segment'][0])
            if ind < (len(sorted_segment_list)):
                BinIntervalTree.construct_max()

    write_output_file(rectangles,'rectangles_count.txt')














