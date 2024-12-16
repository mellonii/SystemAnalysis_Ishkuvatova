import json
import argparse

# вычисления значений функций принадлежности для заданных элементов множества (фаззификации)
def fuzzify(temp, temperature_mfs):
    temp_category = {}

    for category in temperature_mfs:
        membership = 0
        points = category["points"]
        for i in range(len(points) - 1):
            x1, y1 = points[i]
            x2, y2 = points[i + 1]

            if x1 <= temp <= x2:
                if y1 == y2:  # Константное значение
                    membership = max(membership, y1)
                else:  # Линейная интерполяция
                    membership = max(membership, y1 + (y2 - y1) * (temp - x1) / (x2 - x1))

        temp_category[category["id"]] = membership

    print(temp_category)
    return temp_category

# значений функций принадлежности активированного правила
def heating_level(temp_category, rules):
    dict_rules = {}
    for tmp in rules:
        dict_rules[tmp[0]] = tmp[1]

    heat_category = {}
    for t, membership in temp_category.items():
        heat = dict_rules[t]
        heat_category[heat] = membership

    print(heat_category)
    return heat_category

# аккумулирования (объединения) нечетких множеств, полученных при применении уровней активации
def accumulate(heat_category, heating_mfs):
    accumulated_points = []

    for term, membership in heat_category.items():
        for tmp in heating_mfs:
            if tmp["id"] == term:
                points = tmp["points"]
                break
        for x, y in points:
            accumulated_points.append((x, min(membership, y)))
    return accumulated_points

# вычисления (дефаззификация) итогового значения управления
def defuzzify(heat_category, heating_mfs):
    accumulated_points = accumulate(heat_category, heating_mfs)

    max_y = 0
    max_x = 0
    for x, y in accumulated_points:
        if y == max_y and max_x > x:
            max_x = x
        if y > max_y:
            max_y = y
            max_x = x
    return max_x

# алгоритм нечеткого управления
# алгоритм, который для некоторой системы управления температурой в помещении вычисляет параметр управления для поддержания комфортной температуры
def main(temp_json, heat_json, rules_json, temp):
    temperature_mfs = json.loads(temp_json)["температура"]
    heating_mfs = json.loads(heat_json)["температура"]
    rules = json.loads(rules_json)

    temp_category = fuzzify(temp, temperature_mfs)
    heat_category = heating_level(temp_category, rules)
    optimal_s = defuzzify(heat_category, heating_mfs)

    return optimal_s # должна возвращать вещественное число значения оптимального управления

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Обработка четырех JSON-файлов")
    parser.add_argument(
        "temp_file",
        nargs="?",
        default="task6/temp.json",
        help="json-файл с описанием функций принадлежности нечетких множеств термов лингвистической переменной “температура”",
    )
    parser.add_argument(
        "heat_file",
        nargs="?",
        default="task6/heat.json",
        help="json-файл с описанием функций принадлежности нечетких множеств термов лингвистической переменной “уровень нагрева”",
    )
    parser.add_argument(
        "rules_file",
        nargs="?",
        default="task6/rules.json",
        help="json-файл с описанием с описанием логического правила нечеткого управления",
    )
    parser.add_argument(
        "temp",
        nargs="?",
        default=17,
        help="текущее значение температуры (вещественное число), градусов Цельсияы",
    )
    args = parser.parse_args()

    with open(args.temp_file, "r", encoding="utf-8") as file:
        temp_json = file.read()
    with open(args.heat_file, "r", encoding="utf-8") as file:
        heat_json = file.read()
    with open(args.rules_file, "r", encoding="utf-8") as file:
        rules_json = file.read()

    print(main(temp_json, heat_json, rules_json, float(args.temp)))