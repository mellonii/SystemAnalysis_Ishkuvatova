import json
import numpy as np
import argparse

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

def to_matrix(ribs):
    n = len(ribs) + 1
    matrix = np.zeros((n,n), dtype=int)
    for x in ribs:
        a = x[0] - 1
        b = x[1] - 1
        matrix[a][b] = 1
        matrix[b][a] = 1
    return matrix

def to_array(ribs):
    n = len(ribs) + 1
    array = np.zeros(n)
    for x in ribs:
        a = x[0]
        b = x[1] - 1
        array[b] = a
    return array

def main(json_string=None):

    tree = json_to_tree(json_string)
    print("Список связей (ребра):")
    print(tree)
    print("\nМатрица смежности:")
    print(to_matrix(tree))
    print("\nМассив родительских узлов:")
    print(to_array(tree))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Обработка JSON-дерева")
    parser.add_argument(
        "file",
        nargs="?",
        default="task1/tree.json",
        help="Путь к JSON-файлу (по умолчанию tree.json)",
    )
    args = parser.parse_args()

    with open(args.file, "r") as file:
        json_string = file.read()

    main(json_string)  