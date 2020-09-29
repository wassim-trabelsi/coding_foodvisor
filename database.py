#!usr/bin/python
# -*- coding: utf-8 -*-


class Node(object):

    def __init__(self, id):
        self.id = id
        self.isleaf = True
        self.childs = []
        self.images = []

    def add_child(self, child):
        self.childs.append(child)
        self.isleaf = False

    def add_childs(self, childs):
        for child in childs:
            self.add_child(child)

    def add_image(self, image):
        self.images.append(image)


class Database(object):

    def __init__(self, root_id='core'):
        # Root of the database
        self.root = Node(root_id)
        # Dict of registered nodes
        self.id2node = {root_id: self.root}
        # Dict of registered images and their corresponding labels
        self.image2labels = {}
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
        # Update extract
        coverage_images = [image for sister in father.childs for image in sister.images]
        granularity_images = father.images
        self.update_extract(coverage_images, granularity_images)

    def update_extract(self, coverage_images, granularity_images):
        for image in granularity_images:
            if self.extract[image] in ['valid', 'granularity_staged']:
                self.extract[image] = 'granularity_staged'
        for image in coverage_images:
            if self.extract[image] in ['valid', 'granularity_staged', 'coverage_staged']:
                self.extract[image] = 'coverage_staged'

    def add_extract(self, image2labels):
        """
        The add_extract method takes a dict as input where the keys are image names,
        and values are list of node IDs (string).
        """
        # Save the image2labels
        self.image2labels = image2labels
        # Reset extract
        self.reset_extract()

    def reset_extract(self):
        self.extract = {}
        for image, labels in self.image2labels.items():
            # Check if all labels exist, otherwise it's invalid
            if all([label_id in self.id2node for label_id in labels]):
                # Check if all labels are at the last level of granularity
                last_level_granularity = []
                for label_id in labels:
                    label_node = self.id2node[label_id]
                    label_node.add_image(image)
                    last_level_granularity.append(label_node.isleaf)
                if all(last_level_granularity):
                    self.extract[image] = 'valid'
                else:
                    self.extract[image] = 'granularity_staged'
            else:
                self.extract[image] = 'invalid'

    def get_extract_status(self):
        return self.extract
