#!usr/bin/python
# -*- coding: utf-8 -*-


class Node(object):

    def __init__(self, id, childs=[]):
        self.id = id
        self.isleaf = True
        self.childs = childs

        if len(self.childs) > 0:
            self.leaf = False

    def add_child(self, child):
        self.childs.append(child)
        self.isleaf = False

    def add_childs(self, childs):
        for child in childs:
            self.add_child(child)


class Database(object):

    def __init__(self, root_id='core'):
        # Root of the database
        self.root = Node(root_id)
        # Dict of registered nodes
        self.id2node = {root_id: self.root}
        # Reset extract
        self.extract = {}

    def add_nodes(self, nodes):
        """
        The add_nodes method takes a list of tuples as input.
        Each tuple has two elements: the first being the ID of a new node,
        and the second the ID of the parent node.
        """
        for node in nodes:
            self.add_node(node)

    def add_node(self, node):
        child_id, father_id = node

        if child_id in self.id2node:
            print('Warning !! {} is already registered, cannot add this id : skipped '.format(child_id))
            return

        if father_id not in self.id2node:
            print('Warning !! {} is not registered, cannot add granularity : skipped '.format(father_id))
            return

        # Create the child node
        child = Node(child_id)
        # Update the dictionary
        self.id2node[child_id] = child
        # Get the father
        father = self.id2node[father_id]
        # Add the child to his father
        father.add_child(child)

    def add_extract(self, image2labels):
        """
        The add_extract method takes a dict as input where the keys are image names,
        and values are list of node IDs (string).
        """
        # Reset extract
        self.extract = {}
        for image, labels in image2labels.items():
            # Check if all labels exist
            if all([label in self.id2node for label in labels]):
                # Check if all labels are at the last level of granularity
                if all([self.id2node[label].isleaf for label in labels]):
                    self.extract[image] = 'valid'
                else:
                    self.extract[image] = 'granularity_staged'
            else:
                self.extract[image] = 'invalid'

    def update_extract(self):
        pass

    def get_extract_status(self):
        return self.extract
