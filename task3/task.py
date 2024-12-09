import json
import numpy as np
import argparse
import math

def dict_to_tree(result, tree, parent):
    for x in tree:
        for i in tree[x]:
            result.append([int(x), int(i)])
        dict_to_tree(result, tree[x], x)

def json_to_tree(json_data):
    result = []
    tree = json.loads(json_data)
    dict_to_tree(result, tree, 0)
    return result

class Tree:
    # Корень дерева
    root = None

    def __init__(self, value):
        self.value = value
        self.parent = None
        self.children = []

    def add_child(self, child_node):
        self.children.append(child_node)
        child_node.parent = self

def build_tree(edges):
    nodes = {}

    for parent, child in edges:
        if parent not in nodes:
            nodes[parent] = Tree(parent)

        if child not in nodes:
            nodes[child] = Tree(child)

        parent_node = nodes[parent]
        child_node = nodes[child]
        parent_node.add_child(child_node)

    Tree.root = nodes[edges[0][0]]
    return nodes

def find_ancestors(node): # r1 - отношение непосредственного управления (прямые предки)
    if node is Tree.root:
        return []
    
    return [node.parent.value]

def find_descendants(node): # r2 - отношение непосредственного подчинения (прямые потомки)
    result = []
    for tmp in node.children:
        if tmp is not None:
            result.append(tmp.value)
    return result

def find_indirect_ancestors(child, node): # r3 - отношение опосредованного управления (непрямые предки)
    ancestors = []
    
    if node is not Tree.root:
        if node is not child:
            ancestors.append(node.parent.value)
        ancestors += find_indirect_ancestors(child, node.parent)

    return ancestors

def find_indirect_descendants(parent, node): # r4 - отношение опосредованного подчинения (непрямые потомки)
    descendants = []
    
    for child in node.children:
        if child is not None:
            if node is not parent:
                descendants.append(child.value)
            descendants += find_indirect_descendants(parent, child)

    return descendants

def bro_and_sis(node): # r5 - отношение соподчинения на одном уровне (братья и сестры)
    if node is Tree.root:
        return []
    
    parent = node.parent
    result = []

    for tmp in parent.children:
        if (tmp != node): 
            result.append(tmp.value)

    return result

def main(json_string=None):
    edges = json_to_tree(json_string)
    tree = build_tree(edges) # словарь с названием и вершиной

    matrix = []
    for node in tree:
        tmp = []
        tmp.append(len(find_ancestors(tree[node]))) # прямые предки
        tmp.append(len(find_descendants(tree[node]))) # прямые потомки
        tmp.append(len(find_indirect_ancestors(tree[node], tree[node]))) # непрямые предки
        tmp.append(len(find_indirect_descendants(tree[node], tree[node]))) # непрямые потомки
        tmp.append(len(bro_and_sis(tree[node]))) # братья и сестры
        matrix.append(tmp)
    
    gamma = len(tree)
    p = 1/(gamma - 1)
    
    H = 0
    for tmp in matrix:
        for x in tmp:
            if x != 0:
                H -= p*x*math.log2(p*x)

    print(H)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Обработка JSON-дерева")
    parser.add_argument(
        "file",
        nargs="?",
        default="/tree.json",
        help="Путь к JSON-файлу (по умолчанию tree.json)",
    )
    args = parser.parse_args()

    with open(args.file, "r") as file:
        json_string = file.read()

    main(json_string)  