import json
import numpy as np
import argparse

# Находит ядро противоречий
def find_S(A, B):
    # Находим матрицы отношений
    Y_a = find_Y(A)
    Y_b = find_Y(B)
    # Находим транспонированные матрицы отношений
    Y_ta = np.transpose(Y_a)
    Y_tb = np.transpose(Y_b)
    # Перемножаем матрицы отношений
    Y_AB = np.multiply(Y_a, Y_b)
    Y_tAB = np.multiply(Y_ta, Y_tb)

    # Находим ядро противоречий
    n = len(Y_a)
    S = []
    for i in range(n):
        for j in range(n):
            if i < j and Y_AB[i, j] == 0 and Y_tAB[i, j] == 0:
                S.append((i + 1, j + 1))

    return S

# Находит матрицу отношений
def find_Y(ranking): 
    levels = {} # Словарь вида {номер: уровень}
    for i, x in enumerate(ranking):
        if isinstance(x, list):
            for item in x:
                levels[item] = i
        else:
            levels[x] = i
    
    n = len(levels)
    matrix = np.zeros((n, n), dtype=int)

    for i in range(1, n + 1):
        for j in range(1, n + 1):
            if levels[j] >= levels[i]:
                matrix[i-1, j-1] = 1

    return matrix

def main(str_A, str_B):
    A = json.loads(str_A)
    B = json.loads(str_B)

    # Находим ядро противоречий
    S = find_S(A, B)
    S_json = json.dumps(S)
    print(S_json)
    return S_json

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Обработка двух JSON-файлов")
    parser.add_argument(
        "file_A",
        nargs="?",
        default="task5/A.json",
        help="Путь к первому JSON-файлу (по умолчанию /A.json)",
    )
    parser.add_argument(
        "file_B",
        nargs="?",
        default="task5/B.json",
        help="Путь ко второму JSON-файлу (по умолчанию /B.json)",
    )
    args = parser.parse_args()

    with open(args.file_A, "r") as file:
        str_A = file.read()
    with open(args.file_B, "r") as file:
        str_B = file.read()

    main(str_A, str_B)